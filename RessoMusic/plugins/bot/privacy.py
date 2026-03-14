import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from RessoMusic import app
import config

# ================================
#        DATABASE SETUP
# ================================
try:
    from RessoMusic.core.mongo import mongodb as db
except ImportError:
    try:
        from RessoMusic.utils.database import mongodb as db
    except ImportError:
        from RessoMusic.core.mongo import mongodb
        db = mongodb

start_img_db = db.start_img_config # Linked to /setstart image

# ================================
#      PREMIUM EMOJIS (14 EIDS)
# ================================
EIDS = [
    6151981777490548710, 6152433938762570514, 6152142357727811958, 6152420392435718199,
    6152351737383493164, 5039727604517570274, 5042302287087666158, 6309745512639633760,
    6307798999101347420, 6307346833534359338, 6307821174017496029, 6307373208928531138,
    6307358404176254008, 6111778259374971023
]

def get_vip():
    return f'<emoji id="{random.choice(EIDS)}">🦋</emoji>'

async def get_start_image():
    data = await start_img_db.find_one({"_id": "start_pic"})
    if data and "file_id" in data:
        return data["file_id"]
    return "https://files.catbox.moe/x832ly.jpg" # Default ANU Image

# ================================
#      /PRIVACY COMMAND (HARD)
# ================================
@app.on_message(filters.command("privacy"))
async def privacy(client, message: Message):
    final_pic = await get_start_image()
    bot_username = app.username
    
    # 🌟 HARDCORE ANU MATRIX UI
    anu_privacy = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} **ᴀɴᴜ ᴍᴀᴛʀɪx ᴩʀɪᴠᴀᴄʏ**\n"
        f"┠ {get_vip()} {get_vip()} {get_vip()}\n"
        f"┠ ʏᴏᴜʀ ᴅᴀᴛᴀ ɪꜱ 100% ꜱᴇᴄᴜʀᴇ.\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} **ᴏᴜʀ ꜱᴛʀɪᴄᴛ ᴩᴏʟɪᴄʏ:**\n"
        f"┠ ⇛ **ɴᴏ ʟᴏɢɢɪɴɢ:** ᴡᴇ ᴅᴏ ɴᴏᴛ ʀᴇᴄᴏʀᴅ ᴠᴄ ᴀᴜᴅɪᴏ.\n"
        f"┠ ⇛ **ᴇɴᴄʀʏᴩᴛᴇᴅ:** ᴀʟʟ Qᴜᴇʀɪᴇꜱ ᴀʀᴇ ᴩʀɪᴠᴀᴛᴇ.\n"
        f"┠ ⇛ **ɴᴏ ꜱᴩᴀᴍ:** ᴡᴇ ɴᴇᴠᴇʀ ꜱᴇʟʟ ʏᴏᴜʀ ᴅᴀᴛᴀ.\n"
        f"┠ ⇛ **ꜱᴀꜰᴇ:** ᴀʙꜱᴏʟᴜᴛᴇʟʏ ꜱᴀꜰᴇ ꜰᴏʀ ɢʀᴏᴜᴩꜱ.\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┠ 🖤 **ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꜱʏꜱᴛᴇᴍ**"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⚖️ ˹ ꜰ ᴜ ʟ ʟ  ᴩ ᴏ ʟ ɪ ᴄ ʏ ˼", url="https://t.me/BMW_USERBOT_II")
            ],
            [
                InlineKeyboardButton("🕷️ ˹ ꜱ ᴜ ᴩ ᴩ ᴏ ʀ ᴛ ˼", url="https://t.me/BMW_USERBOT_II"),
                InlineKeyboardButton("🦇 ˹ ᴍ ʏ  ʜ ᴏ ᴍ ᴇ ˼", url="https://t.me/FUCK_BY_REFLEX")
            ]
        ]
    )

    # Ab reply_text ki jagah reply_photo aayega!
    await message.reply_photo(
        photo=final_pic,
        caption=anu_privacy, 
        reply_markup=keyboard
    )
