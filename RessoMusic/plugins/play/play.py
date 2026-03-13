import random
import string
import urllib.parse
import aiohttp

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from RessoMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from RessoMusic.core.call import AMBOTOP
from RessoMusic.utils import seconds_to_min, time_to_seconds
from RessoMusic.utils.channelplay import get_channeplayCB
from RessoMusic.utils.decorators.language import languageCB
from RessoMusic.utils.decorators.play import PlayWrapper
from RessoMusic.utils.formatters import formats
from RessoMusic.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from RessoMusic.utils.logger import play_logs
from RessoMusic.utils.stream.stream import stream
from config import BANNED_USERS, lyrical

# ==========================================
# 🦋 PREMIUM POOKIE EMOJIS (Random Generator)
# ==========================================
P_EMOJIS = [
    "<emoji id=6151981777490548710>🦋</emoji>",
    "<emoji id=6152433938762570514>🎀</emoji>",
    "<emoji id=6152142357727811958>✨</emoji>",
    "<emoji id=6152420392435718199>🌸</emoji>",
    "<emoji id=6152351737383493164>🥺</emoji>",
    "<emoji id=5039727604517570274>❤️</emoji>",
    "<emoji id=5042302287087666158>💖</emoji>",
    "<emoji id=6309745512639633760>🤍</emoji>",
    "<emoji id=6307798999101347420>🥀</emoji>",
    "<emoji id=6307346833534359338>🍷</emoji>",
    "<emoji id=6307821174017496029>🥂</emoji>",
    "<emoji id=6307373208928531138>😈</emoji>",
    "<emoji id=6307358404176254008>🔥</emoji>",
    "<emoji id=6111778259374971023>👑</emoji>"
]

# ==========================================
# ☠️ CUSTOM BUTTONS (Monster x Reflex)
# ==========================================
def get_custom_buttons():
    return [
        [InlineKeyboardButton(f"🌸 ᴍʏ ᴄʟᴜʙ", url="https://t.me/FUCK_BY_REFLEX")],
        [
            InlineKeyboardButton(f"😈 ʏᴏᴜʀ ᴅᴀᴅ", url="https://t.me/MONSTER_FUCK_BITCHES"),
            InlineKeyboardButton(f"☠️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ", url="https://t.me/MONSTER_FUCK_BITCHES")
        ],
        [InlineKeyboardButton(f"🗑 ᴄʟᴏsᴇ", callback_data="close")]
    ]

# ==========================================
# 🎨 CUSTOM THUMBNAIL LOGIC (/setply)
# ==========================================
CUSTOM_THUMB = None

@app.on_message(filters.command("setply") & filters.user(config.OWNER_ID))
async def set_ply_cmd(client, message):
    global CUSTOM_THUMB
    if len(message.command) < 2:
        return await message.reply_text(
            f"{random.choice(P_EMOJIS)} 𝘉𝘢𝘣𝘺, 𝘎𝘪𝘷𝘦 𝘔𝘦 𝘈 𝘓𝘪𝘯𝘬 (𝘛𝘦𝘭𝘦𝘨𝘳𝘢.𝘱𝘩) 𝘛𝘰 𝘚𝘦𝘵 𝘛𝘩𝘶𝘮𝘣𝘯𝘢𝘪𝘭! 🎀"
        )
    CUSTOM_THUMB = message.text.split(None, 1)[1]
    await message.reply_text(
        f"{random.choice(P_EMOJIS)} 𝘠𝘢𝘺! 𝘊𝘶𝘴𝘵𝘰𝘮 𝘛𝘩𝘶𝘮𝘣𝘯𝘢𝘪𝘭 𝘚𝘦𝘵 𝘚𝘶𝘤𝘤𝘦𝘴𝘴𝘧𝘶𝘭𝘭𝘺! 𝘙𝘌𝘍𝘓𝘌𝘟 𝘚𝘺𝘴𝘵𝘦𝘮 𝘜𝘱𝘥𝘢𝘵𝘦𝘥. 😈"
    )

# ==========================================
# 🎵 JIOSAAVN API LOGIC
# ==========================================
JIOSAAVN_CACHE = {}
JIOSAAVN_API = "https://jiosavan-lilac.vercel.app/api/search/songs?query="

async def jiosaavn_play_logic(query):
    cache_key = query.lower().strip()
    if cache_key in JIOSAAVN_CACHE:
        return JIOSAAVN_CACHE[cache_key]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(JIOSAAVN_API + urllib.parse.quote(query), timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    songs = data.get("data", {}).get("results", []) or data.get("results", [])
                    if songs:
                        song = songs[0]
                        stream_url = song["downloadUrl"][-1]["url"] if "downloadUrl" in song else song["downloadUrl"][-1]["link"]
                        title = song["name"].replace("&quot;", '"').replace("&#039;", "'")
                        
                        # Set Custom Thumb if available
                        thumb = CUSTOM_THUMB if CUSTOM_THUMB else (song["image"][-1]["url"] if "image" in song else song["image"][-1]["link"])
                        
                        duration_sec = song.get("duration", 0)
                        mins = int(duration_sec) // 60
                        secs = int(duration_sec) % 60
                        duration_str = f"{mins}:{secs:02d}"

                        result_tuple = (stream_url, title, thumb, duration_str)
                        JIOSAAVN_CACHE[cache_key] = result_tuple
                        return stream_url, title, thumb, duration_str
    except:
        pass
    return None, None, None, None

# ==========================================
# 🚀 MAIN PLAY COMMAND
# ==========================================
@app.on_message(
    filters.command(["play", "vplay", "cplay", "cvplay", "playforce", "vplayforce", "cplayforce", "cvplayforce"], prefixes=["/", "!", "%", ",", "", ".", "@"])
    & filters.group
    & ~BANNED_USERS
)
@PlayWrapper
async def play_commnd(client, message: Message, _, chat_id, video, channel, playmode, url, fplay):
    
    # 🔥 HACKER POOKIE UI STRING
    mystic = await message.reply_text(
        f"{random.choice(P_EMOJIS)} 𝖲𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀 𝖸𝗈𝗎𝗋 𝖲𝗈𝗇𝗀 𝖡𝖺𝖻𝗒... 𝖯𝗅𝖾𝖺𝗌𝖾 𝖶𝖺𝗂𝗍 𝖬𝗒 𝖫𝗈𝗋𝖽 😈"
    )
    
    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    audio_telegram = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    video_telegram = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None

    # Handle Audio/Video from Telegram...
    if audio_telegram:
        if audio_telegram.file_size > 104857600:
            return await mystic.edit_text(f"{random.choice(P_EMOJIS)} 𝖥𝗂𝗅𝖾 𝖳𝗈𝗈 𝖡𝗂𝗀 𝖡𝖺𝖻𝗒! 𝖲𝖾𝗇𝖽 𝖲𝗆𝖺𝗅𝗅𝖾𝗋 𝖮𝗇𝖾. 🥺")
        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram, file_path)
            details = {"title": file_name, "link": message_link, "path": file_path, "dur": dur}
            try:
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, streamtype="telegram", forceplay=fplay)
            except Exception as e:
                return await mystic.edit_text(f"{random.choice(P_EMOJIS)} 𝖤𝗋𝗋𝗈𝗋 𝖮𝖼𝖼𝗎𝗋𝖾𝖽: {e}")
            return await mystic.delete()
        return

    elif url:
        if await YouTube.exists(url):
            try:
                details, track_id = await YouTube.track(url)
            except:
                return await mystic.edit_text(f"{random.choice(P_EMOJIS)} 𝖲𝗈𝗇𝗀 𝖭𝗈𝗍 𝖥𝗈𝗎𝗇𝖽 𝖡𝖺𝖻𝗒! 🥺")
            streamtype = "youtube"
            img = CUSTOM_THUMB if CUSTOM_THUMB else details["thumb"]
            cap = f"{random.choice(P_EMOJIS)} **{details['title']}**"
        
        # JioSaavn Direct Play Logic Bypass
    else:
        if len(message.command) < 2:
            return await mystic.edit_text(
                f"{random.choice(P_EMOJIS)} 𝘉𝘢𝘣𝘺, 𝘗𝘭𝘦𝘢𝘴𝘦 𝘎𝘪𝘷𝘦 𝘈 𝘚𝘰𝘯𝘨 𝘕𝘢𝘮𝘦 𝘛𝘰 𝘗𝘭𝘢𝘺! 🎀",
                reply_markup=InlineKeyboardMarkup(get_custom_buttons())
            )
        slider = True
        query = message.text.split(None, 1)[1]
        if "-v" in query:
            query = query.replace("-v", "")

        if str(playmode) == "Direct" and not video:
            stream_url, js_title, js_thumb, js_dur = await jiosaavn_play_logic(query)
            if stream_url:
                details = {
                    "title": js_title,
                    "link": stream_url,
                    "path": stream_url,
                    "dur": js_dur,
                    "duration_min": js_dur,
                    "thumb": CUSTOM_THUMB if CUSTOM_THUMB else js_thumb
                }
                try:
                    await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=video, streamtype="telegram", forceplay=fplay)
                    await mystic.delete()
                    return await play_logs(message, streamtype="JioSaavn")
                except Exception:
                    pass 

        try:
            details, track_id = await YouTube.track(query)
            details["thumb"] = CUSTOM_THUMB if CUSTOM_THUMB else details["thumb"]
        except:
            return await mystic.edit_text(f"{random.choice(P_EMOJIS)} 𝖲𝗈𝗇𝗀 𝖭𝗈𝗍 𝖥𝗈𝗎𝗇𝖽 𝖡𝖺𝖻𝗒! 🥺")
        streamtype = "youtube"

    if str(playmode) == "Direct":
        try:
            await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=video, streamtype=streamtype, spotify=spotify, forceplay=fplay)
        except Exception as e:
            return await mystic.edit_text(f"{random.choice(P_EMOJIS)} 𝖤𝗋𝗋𝗈𝗋 𝖮𝖼𝖼𝗎𝗋𝖾𝖽: {e}")
        await mystic.delete()
        return await play_logs(message, streamtype=streamtype)
    else:
        if slider:
            await mystic.delete()
            await message.reply_photo(
                photo=CUSTOM_THUMB if CUSTOM_THUMB else details["thumb"],
                has_spoiler=True,
                caption=f"{random.choice(P_EMOJIS)} 𝖲𝗈𝗇𝗀: **{details['title'].title()}**\n⏳ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇: {details['duration_min']}",
                reply_markup=InlineKeyboardMarkup(get_custom_buttons())
            )
            return await play_logs(message, streamtype=f"Searched on Youtube")

# KEEP OTHER CALLBACKS INTACT
@app.on_callback_query(filters.regex("AnonymousAdmin") & ~BANNED_USERS)
async def anonymous_check(client, CallbackQuery):
    try:
        await CallbackQuery.answer("» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ʙᴀʙʏ 🎀", show_alert=True)
    except:
        pass
