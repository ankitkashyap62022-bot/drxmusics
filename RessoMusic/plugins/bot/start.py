import asyncio
import random
import time
from pyrogram import filters, enums
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message, CallbackQuery
from youtubesearchpython.__future__ import VideosSearch

import config
from RessoMusic import app
from RessoMusic.misc import _boot_
from RessoMusic.plugins.sudo.sudoers import sudoers_list
from RessoMusic.utils import bot_sys_stats
from RessoMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)

# --- DATABASE ---
try:
    from RessoMusic.core.mongo import mongodb as db
except ImportError:
    try:
        from RessoMusic.utils.database import mongodb as db
    except ImportError:
        from RessoMusic.core.mongo import mongodb
        db = mongodb

from RessoMusic.utils.decorators.language import LanguageStart
from RessoMusic.utils.formatters import get_readable_time
from config import BANNED_USERS
from strings import get_string

# ================================
#        DATABASE SETUP
# ================================
welcome_db = db.welcome_config 
start_img_db = db.start_img_config 

# ================================
#      PREMIUM EMOJIS & ASSETS
# ================================
EIDS = [
    6151981777490548710, 6152433938762570514, 6152142357727811958, 6152420392435718199,
    6152351737383493164, 5039727604517570274, 5042302287087666158, 6309745512639633760,
    6307798999101347420, 6307346833534359338, 6307821174017496029, 6307373208928531138,
    6307358404176254008, 6111778259374971023
]

def get_vip():
    return f'<emoji id="{random.choice(EIDS)}">🦋</emoji>'

DEFAULT_START_PIC = "https://files.catbox.moe/x832ly.jpg"

async def get_start_image():
    data = await start_img_db.find_one({"_id": "start_pic"})
    if data and "file_id" in data:
        return data["file_id"]
    return DEFAULT_START_PIC

# ================================
#      DARK INLINE BUTTONS (UI)
# ================================
def anu_private_panel():
    return [
        [
            InlineKeyboardButton(text="🕷️ ꜱᴜᴩᴩᴏʀᴛ ɢʀᴏᴜᴩ", url="https://t.me/BMW_USERBOT_II"),
            InlineKeyboardButton(text="🦇 ᴍʏ ʜᴏᴍᴇ", url="https://t.me/FUCK_BY_REFLEX")
        ],
        [
            InlineKeyboardButton(text="💀 ᴍʏ ᴍᴀꜱᴛᴇʀ", url="https://t.me/MONSTER_FUCK_BITCHES")
        ],
        [
            InlineKeyboardButton(text="🍷 ᴄᴏᴍᴍᴀɴᴅꜱ & ʜᴇʟᴩ", callback_data="anu_help_menu")
        ]
    ]

def anu_group_panel():
    return [
        [
            InlineKeyboardButton(text="🕷️ ꜱᴜᴩᴩᴏʀᴛ", url="https://t.me/BMW_USERBOT_II"),
            InlineKeyboardButton(text="🦇 ᴍʏ ʜᴏᴍᴇ", url="https://t.me/FUCK_BY_REFLEX")
        ]
    ]

# ================================
#      /SETSTART IMAGE COMMAND
# ================================
@app.on_message(filters.command(["setstart"]) & filters.user(config.OWNER_ID))
async def set_start_img(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text(f"{get_vip()} **[ ꜱʏꜱᴛᴇᴍ ᴀʟᴇʀᴛ ]**\n\n`ʀᴇᴩʟʏ ᴛᴏ ᴀɴʏ ɪᴍᴀɢᴇ ᴡɪᴛʜ /setstart ᴛᴏ ᴏᴠᴇʀʀɪᴅᴇ ᴅᴀᴛᴀʙᴀꜱᴇ.`")
    
    file_id = message.reply_to_message.photo.file_id
    await start_img_db.update_one({"_id": "start_pic"}, {"$set": {"file_id": file_id}}, upsert=True)
    await message.reply_text(f"{get_vip()} **[ ᴀɴᴜ ᴍᴀɪɴꜰʀᴀᴍᴇ ]**\n\n`ɴᴇᴡ ꜱᴛᴀʀᴛ ɪᴍᴀɢᴇ ɪɴᴊᴇᴄᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ.`")

# ================================
#        START COMMAND (DM)
# ================================
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    # --- DARK BOOTING ANIMATION ---
    anim = await message.reply_text(f"▰▱▱▱▱ {get_vip()} `[ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴀɴᴜ ᴄᴏʀᴇ... ]`")
    await add_served_user(message.from_user.id)
    await asyncio.sleep(0.3)
    await anim.edit_text(f"▰▰▰▱▱ {get_vip()} `[ ʙʏᴩᴀꜱꜱɪɴɢ ꜱᴇᴄᴜʀɪᴛʏ ᴩʀᴏᴛᴏᴄᴏʟꜱ... ]`")
    await asyncio.sleep(0.3)
    await anim.edit_text(f"▰▰▰▰▰ {get_vip()} `[ ᴀɴᴜ ᴍᴀɪɴꜰʀᴀᴍᴇ ᴏɴʟɪɴᴇ. ]`")
    await anim.delete()

    UP, CPU, RAM, DISK = await bot_sys_stats()
    start_pic = await get_start_image()
    
    caption = (
        f"{get_vip()} **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ**\n\n"
        f"❝ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴅᴀʀᴋ ꜱɪᴅᴇ, {message.from_user.mention} ❞\n\n"
        f"ɪ ᴀᴍ {app.mention}, ᴀ ʟᴇᴛʜᴀʟ ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜꜱɪᴄ ᴇɴɢɪɴᴇ ᴅᴇꜱɪɢɴᴇᴅ ᴛᴏ ᴅᴏᴍɪɴᴀᴛᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ.\n\n"
        f"🖧 **ꜱᴇʀᴠᴇʀ ꜱᴛᴀᴛꜱ:**\n"
        f"⇛ ᴜᴩᴛɪᴍᴇ: `{UP}`\n"
        f"⇛ ʀᴀᴍ: `{RAM}` | ᴅɪꜱᴋ: `{DISK}`\n\n"
        f"🖤 **ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꭙ ꜱʏꜱᴛᴇᴍ**"
    )

    await message.reply_photo(
        photo=start_pic,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(anu_private_panel()),
    )

    if await is_on_off(2):
        await app.send_message(
            chat_id=config.LOGGER_ID,
            text=f"❖ ᴀ ɴᴇᴡ ᴜꜱᴇʀ ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ᴍᴀᴛʀɪx.\n\n<b>๏ ᴜsᴇʀ :</b> {message.from_user.mention}\n<b>๏ ɪᴅ :</b> <code>{message.from_user.id}</code>",
        )

# ================================
#        START COMMAND (GROUP)
# ================================
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    uptime = int(time.time() - _boot_)
    start_pic = await get_start_image()
    
    caption = (
        f"{get_vip()} **ᴀɴᴜ ᴍᴀᴛʀɪx ɪꜱ ᴀʟɪᴠᴇ.**\n\n"
        f"ꜱʏꜱᴛᴇᴍꜱ ᴀʀᴇ ʀᴜɴɴɪɴɢ ꜱᴍᴏᴏᴛʜʟʏ.\n"
        f"⇛ ᴜᴩᴛɪᴍᴇ: `{get_readable_time(uptime)}`\n\n"
        f"🖤 **ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꭙ ꜱʏꜱᴛᴇᴍ**"
    )

    await message.reply_photo(
        photo=start_pic,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(anu_group_panel()),
    )
    return await add_served_chat(message.chat.id)


# ================================
#     HELP MENU CALLBACKS (UI)
# ================================
@app.on_callback_query(filters.regex("^anu_help_") & ~BANNED_USERS)
async def help_menu_callbacks(client, query: CallbackQuery):
    data = query.data
    
    # 🔙 BACK BUTTON / MAIN MENU
    if data == "anu_help_menu":
        caption = (
            f"{get_vip()} **ᴀɴᴜ ᴄᴏᴍᴍᴀɴᴅ ᴍᴀɪɴꜰʀᴀᴍᴇ**\n\n"
            f"ꜱᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ᴛᴏ ᴀᴄᴄᴇꜱꜱ ᴛʜᴇ ᴄᴏɴᴛʀᴏʟ ᴩᴀɴᴇʟ."
        )
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🗡️ ᴀᴅᴍɪɴ", callback_data="anu_help_admin"),
                InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", callback_data="anu_help_owner")
            ],
            [
                InlineKeyboardButton("🎵 ᴩʟᴀʏ", callback_data="anu_help_play")
            ],
            [
                InlineKeyboardButton("🔙 ʀᴇᴛᴜʀɴ", callback_data="anu_help_close")
            ]
        ])
        await query.message.edit_caption(caption=caption, reply_markup=keyboard)

    # 🗡️ ADMIN COMMANDS
    elif data == "anu_help_admin":
        caption = (
            f"{get_vip()} **ᴀɴᴜ ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟꜱ**\n\n"
            f"⇛ `/pause` - ᴩᴀᴜꜱᴇ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ.\n"
            f"⇛ `/resume` - ʀᴇꜱᴜᴍᴇ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ.\n"
            f"⇛ `/skip` - ꜱᴋɪᴩ ᴛᴏ ɴᴇxᴛ ᴛʀᴀᴄᴋ.\n"
            f"⇛ `/stop` - ꜱᴛᴏᴩ ᴍᴜꜱɪᴄ & ʟᴇᴀᴠᴇ ᴠᴄ.\n"
            f"⇛ `/mute` - ᴍᴜᴛᴇ ᴀ ᴜꜱᴇʀ.\n"
            f"⇛ `/unmute` - ᴜɴᴍᴜᴛᴇ ᴀ ᴜꜱᴇʀ.\n"
            f"⇛ `/ban` - ʙᴀɴ ᴀ ᴜꜱᴇʀ ꜰʀᴏᴍ ɢʀᴏᴜᴩ.\n"
            f"⇛ `/unban` - ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ."
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʀᴇᴛᴜʀɴ", callback_data="anu_help_menu")]])
        await query.message.edit_caption(caption=caption, reply_markup=keyboard)

    # 👑 OWNER COMMANDS
    elif data == "anu_help_owner":
        caption = (
            f"{get_vip()} **ᴀɴᴜ ᴏᴡɴᴇʀ ᴏᴠᴇʀʀɪᴅᴇ**\n\n"
            f"⇛ `/gban` - ɢʟᴏʙᴀʟ ʙᴀɴ ᴀ ᴜꜱᴇʀ.\n"
            f"⇛ `/ungban` - ɢʟᴏʙᴀʟ ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ.\n"
            f"⇛ `/broadcast` - ꜱᴇɴᴅ ᴍꜱɢ ᴛᴏ ᴀʟʟ ᴄʜᴀᴛꜱ.\n"
            f"⇛ `/setstart` - ᴄʜᴀɴɢᴇ ꜱᴛᴀʀᴛ ɪᴍᴀɢᴇ.\n"
            f"⇛ `/setwelcome_dm` - ꜱᴇᴛ ᴅᴍ ᴡᴇʟᴄᴏᴍᴇ ᴍꜱɢ.\n"
            f"⇛ `/setwelcome_grp` - ꜱᴇᴛ ɢʀᴏᴜᴩ ᴡᴇʟᴄᴏᴍᴇ ᴍꜱɢ."
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʀᴇᴛᴜʀɴ", callback_data="anu_help_menu")]])
        await query.message.edit_caption(caption=caption, reply_markup=keyboard)

    # 🎵 PLAY COMMANDS
    elif data == "anu_help_play":
        caption = (
            f"{get_vip()} **ᴀɴᴜ ᴍᴜꜱɪᴄ ᴇɴɢɪɴᴇ**\n\n"
            f"⇛ `/play` - ᴩʟᴀʏ ᴀ ꜱᴏɴɢ ɪɴ ᴠᴄ.\n"
            f"⇛ `/vplay` - ᴩʟᴀʏ ᴠɪᴅᴇᴏ ɪɴ ᴠᴄ.\n"
            f"⇛ `/song` - ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ꜱᴏɴɢ.\n"
            f"⇛ `/video` - ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴠɪᴅᴇᴏ.\n"
            f"⇛ `/queue` - ᴄʜᴇᴄᴋ ᴩʟᴀʏ ʟɪꜱᴛ."
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʀᴇᴛᴜʀɴ", callback_data="anu_help_menu")]])
        await query.message.edit_caption(caption=caption, reply_markup=keyboard)

    # 🔙 CLOSE HELP
    elif data == "anu_help_close":
        UP, CPU, RAM, DISK = await bot_sys_stats()
        caption = (
            f"{get_vip()} **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ**\n\n"
            f"❝ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴅᴀʀᴋ ꜱɪᴅᴇ, {query.from_user.mention} ❞\n\n"
            f"ɪ ᴀᴍ {app.mention}, ᴀ ʟᴇᴛʜᴀʟ ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜꜱɪᴄ ᴇɴɢɪɴᴇ ᴅᴇꜱɪɢɴᴇᴅ ᴛᴏ ᴅᴏᴍɪɴᴀᴛᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ.\n\n"
            f"🖤 **ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꭙ ꜱʏꜱᴛᴇᴍ**"
        )
        await query.message.edit_caption(
            caption=caption, 
            reply_markup=InlineKeyboardMarkup(anu_private_panel())
        )
