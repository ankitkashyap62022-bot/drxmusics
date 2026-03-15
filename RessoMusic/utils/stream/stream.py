import os
import random
import asyncio
import requests
from random import randint
from typing import Union

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup

import config
from RessoMusic import Carbon, YouTube, app
from RessoMusic.core.call import AMBOTOP
from RessoMusic.misc import db
from RessoMusic.utils.database import add_active_video_chat, is_active_chat
from RessoMusic.utils.exceptions import AssistantErr
from RessoMusic.utils.inline import aq_markup, close_markup, stream_markup
from RessoMusic.utils.pastebin import AMBOTOPBin
from RessoMusic.utils.stream.queue import put_queue, put_queue_index
from RessoMusic.utils.thumbnails import gen_thumb, get_custom_thumb

# 🔥 MONGODB DATABASE 🔥
from RessoMusic.core.mongo import mongodb

P_EMOJIS = [
    "<emoji id=6151981777490548710>🦋</emoji>", "<emoji id=6152433938762570514>🎀</emoji>",
    "<emoji id=6152142357727811958>✨</emoji>", "<emoji id=6152420392435718199>🌸</emoji>",
    "<emoji id=6152351737383493164>🥺</emoji>", "<emoji id=5039727604517570274>❤️</emoji>",
    "<emoji id=5042302287087666158>💖</emoji>", "<emoji id=6309745512639633760>🤍</emoji>",
    "<emoji id=6307798999101347420>🥀</emoji>", "<emoji id=6307346833534359338>🍷</emoji>",
    "<emoji id=6307821174017496029>🥂</emoji>", "<emoji id=6307373208928531138>😈</emoji>",
    "<emoji id=6307358404176254008>🔥</emoji>", "<emoji id=6111778259374971023>👑</emoji>"
]

def get_vip():
    return random.choice(P_EMOJIS)

# ==========================================
# 🎨 CUSTOM THUMBNAIL UPLOADER LOGIC
# ==========================================
custom_thumb_db = mongodb.custom_thumb

def upload_image_sync(file_path):
    # 1. Try Telegraph
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                "https://telegra.ph/upload", 
                files={"file": ("photo.jpg", f, "image/jpeg")}
            )
        res = response.json()
        if isinstance(res, list) and "src" in res[0]:
            return "https://telegra.ph" + res[0]["src"]
    except Exception as e:
        pass

    # 2. Try Catbox as Fallback
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": f}
            )
        if response.status_code == 200 and response.text.startswith("http"):
            return response.text.strip()
    except Exception as e:
        pass

    return None

async def upload_to_cloud(file_path):
    return await asyncio.to_thread(upload_image_sync, file_path)

@app.on_message(filters.command(["setply", "setphoto"]) & filters.user(config.OWNER_ID))
async def set_ply_cmd(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text(
            f"{get_vip()} ʙᴀʙʏ, ᴋɪsɪ ᴘʜᴏᴛᴏ ᴘᴀʀ ʀᴇᴘʟʏ ᴋᴀʀᴋᴇ /sᴇᴛᴘʜᴏᴛᴏ ʟɪᴋʜᴏ! 🎀"
        )

    mystic = await message.reply_text(f"{get_vip()} 🌸 ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ᴘʜᴏᴛᴏ ᴛᴏ ʀᴇғʟᴇx sᴇʀᴠᴇʀ...")

    local_path = await client.download_media(message.reply_to_message)
    image_url = await upload_to_cloud(local_path)

    if os.path.exists(local_path):
        os.remove(local_path)

    if not image_url:
        return await mystic.edit_text(f"{get_vip()} 🥺 ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ. sᴇʀᴠᴇʀs ᴍɪɢʜᴛ ʙᴇ ᴅᴏᴡɴ! ᴛʀʏ ᴀɢᴀɪɴ.")

    # Update Database
    await custom_thumb_db.update_one({"_id": "custom_thumbnail"}, {"$set": {"url": image_url}}, upsert=True)
    
    # Update Cache instantly
    try:
        import time
        from RessoMusic.utils.thumbnails import _CACHE
        _CACHE["url"] = image_url
        _CACHE["time"] = time.time()
    except:
        pass

    await mystic.edit_text(
        f"{get_vip()} ʏᴀʏ! ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ! ʀᴇғʟᴇx sʏsᴛᴇᴍ ᴜᴘᴅᴀᴛᴇᴅ. 😈\n\n(🔗 ᴜʀʟ: {image_url})"
    )


# ==========================================
# 🚀 STREAM LOGIC WITH SPOILER
# ==========================================
async def stream(_, mystic, user_id, result, chat_id, user_name, original_chat_id, video: Union[bool, str] = None, streamtype: Union[bool, str] = None, spotify: Union[bool, str] = None, forceplay: Union[bool, str] = None):
    if not result:
        return
    if forceplay:
        await AMBOTOP.force_stop_stream(chat_id)

    # 🌟 MASTER OVERRIDE THUMBNAIL
    master_thumb = await get_custom_thumb()
    fallback_image = master_thumb if master_thumb else config.START_IMG_URL 

    if streamtype == "playlist":
        msg = f"{_['play_19']}\n\n"
        count = 0
        for search in result:
            if int(count) == config.PLAYLIST_FETCH_LIMIT:
                continue
            try:
                (title, duration_min, duration_sec, thumbnail, vidid) = await YouTube.details(search, False if spotify else True)
            except:
                continue
            if str(duration_min) == "None" or duration_sec > config.DURATION_LIMIT:
                continue
            if await is_active_chat(chat_id):
                await put_queue(chat_id, original_chat_id, f"vid_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio")
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}. {title[:70]}\n{_['play_20']} {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []
                status = True if video else None
                try:
                    file_path, direct = await YouTube.download(vidid, mystic, video=status, videoid=True)
                except:
                    raise AssistantErr(_["play_14"])
                await AMBOTOP.join_call(chat_id, original_chat_id, file_path, video=status, image=thumbnail)
                await put_queue(chat_id, original_chat_id, file_path if direct else f"vid_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio", forceplay=forceplay)
                
                img = master_thumb if master_thumb else await gen_thumb(vidid)
                button = stream_markup(_, chat_id)
                try:
                    run = await app.send_photo(original_chat_id, photo=img, caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}", title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
                except:
                    run = await app.send_message(original_chat_id, text=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}", title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
        if count == 0:
            return
        else:
            link = await AMBOTOPBin(msg)
            lines = msg.count("\n")
            car = os.linesep.join(msg.split(os.linesep)[:17]) if lines >= 17 else msg
            carbon = await Carbon.generate(car, randint(100, 10000000))
            upl = close_markup(_)
            try:
                return await app.send_photo(original_chat_id, photo=carbon, caption=_["play_21"].format(position, link), reply_markup=upl, has_spoiler=True)
            except:
                pass

    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        thumbnail = result["thumb"]
        status = True if video else None

        current_queue = db.get(chat_id)
        if current_queue is not None and len(current_queue) >= 10:
            return await app.send_message(original_chat_id, f"{get_vip()} ʏᴏᴜ ᴄᴀɴ'ᴛ ᴀᴅᴅ ᴍᴏʀᴇ ᴛʜᴀɴ 10 sᴏɴɢs ᴛᴏ ᴛʜᴇ ǫᴜᴇᴜᴇ.")

        try:
            file_path, direct = await YouTube.download(vidid, mystic, videoid=True, video=status)
        except:
            raise AssistantErr(_["play_14"])

        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path if direct else f"vid_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio")
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(original_chat_id, text=_["queue_4"].format(position, title[:27], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await AMBOTOP.join_call(chat_id, original_chat_id, file_path, video=status, image=thumbnail)
            await put_queue(chat_id, original_chat_id, file_path if direct else f"vid_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio", forceplay=forceplay)
            
            img = master_thumb if master_thumb else await gen_thumb(vidid)
            button = stream_markup(_, chat_id)
            try:
                run = await app.send_photo(original_chat_id, photo=img, caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}", title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            except:
                run = await app.send_message(original_chat_id, text=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}", title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

    elif streamtype == "soundcloud":
        file_path = result["filepath"]
        title = result["title"]
        duration_min = result["duration_min"]
        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "audio")
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(original_chat_id, text=_["queue_4"].format(position, title[:27], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await AMBOTOP.join_call(chat_id, original_chat_id, file_path, video=None)
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "audio", forceplay=forceplay)
            button = stream_markup(_, chat_id)
            try:
                run = await app.send_photo(original_chat_id, photo=fallback_image, caption=_["stream_1"].format(config.SUPPORT_GROUP, title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            except:
                run = await app.send_message(original_chat_id, text=_["stream_1"].format(config.SUPPORT_GROUP, title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        title = (result["title"]).title()
        duration_min = result["dur"]
        
        # 🌟 JIOSAAVN THUMBNAIL FIX
        thumbnail = result.get("thumb", fallback_image)
        status = True if video else None

        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "video" if video else "audio")
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(original_chat_id, text=_["queue_4"].format(position, title[:27], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await AMBOTOP.join_call(chat_id, original_chat_id, file_path, video=status)
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "video" if video else "audio", forceplay=forceplay)
            if video:
                await add_active_video_chat(chat_id)
            button = stream_markup(_, chat_id)
            try:
                run = await app.send_photo(original_chat_id, photo=thumbnail, caption=_["stream_1"].format(link, title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            except:
                run = await app.send_message(original_chat_id, text=_["stream_1"].format(link, title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

    elif streamtype == "live":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        thumbnail = result["thumb"]
        duration_min = "ʟɪᴠᴇ ᴛʀᴀᴄᴋ"
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, f"live_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio")
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(original_chat_id, text=_["queue_4"].format(position, title[:27], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            n, file_path = await YouTube.video(link)
            if n == 0:
                raise AssistantErr(_["str_3"])
            await AMBOTOP.join_call(chat_id, original_chat_id, file_path, video=status, image=thumbnail if thumbnail else None)
            await put_queue(chat_id, original_chat_id, f"live_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio", forceplay=forceplay)
            
            img = master_thumb if master_thumb else await gen_thumb(vidid)
            button = stream_markup(_, chat_id)
            try:
                run = await app.send_photo(original_chat_id, photo=img, caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}", title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            except:
                run = await app.send_message(original_chat_id, text=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}", title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

    elif streamtype == "index":
        link = result
        title = "ɪɴᴅᴇx ᴏʀ ᴍ3ᴜ8 ʟɪɴᴋ"
        duration_min = "00:00"
        if await is_active_chat(chat_id):
            await put_queue_index(chat_id, original_chat_id, "index_url", title, duration_min, user_name, link, "video" if video else "audio")
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await mystic.edit_text(text=_["queue_4"].format(position, title[:27], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await AMBOTOP.join_call(chat_id, original_chat_id, link, video=True if video else None)
            await put_queue_index(chat_id, original_chat_id, "index_url", title, duration_min, user_name, link, "video" if video else "audio", forceplay=forceplay)
            button = stream_markup(_, chat_id)
            try:
                run = await app.send_photo(original_chat_id, photo=fallback_image, caption=_["stream_2"].format(user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            except:
                run = await app.send_message(original_chat_id, text=_["stream_2"].format(user_name), reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await mystic.delete()
            
