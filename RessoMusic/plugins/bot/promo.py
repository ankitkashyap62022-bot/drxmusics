import random
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from RessoMusic import app
from RessoMusic.misc import SUDOERS

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

promo_db = db.promo_config # Database for /setpromo

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

# ================================
#      /SETPROMO IMAGE COMMAND
# ================================
@app.on_message(filters.command(["setpromo"]) & SUDOERS)
async def set_promo_img(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text(f"{get_vip()} **[ ꜱʏꜱᴛᴇᴍ ᴀʟᴇʀᴛ ]**\n\n`ʙᴀʙʏ, ᴋɪꜱɪ ᴩʜᴏᴛᴏ ᴩᴇ ʀᴇᴩʟʏ ᴋᴀʀᴋᴇ /setpromo ʟɪᴋʜᴏ!`")
    
    file_id = message.reply_to_message.photo.file_id
    await promo_db.update_one({"_id": "promo_pic"}, {"$set": {"file_id": file_id}}, upsert=True)
    await message.reply_text(f"{get_vip()} **[ ᴀɴᴜ ᴍᴀɪɴꜰʀᴀᴍᴇ ]**\n\n`ᴩʀᴏᴍᴏ ɪᴍᴀɢᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴜᴩᴅᴀᴛᴇᴅ! ᴀʙ /promo ᴩᴇ ʏᴀʜɪ ᴩʜᴏᴛᴏ ᴀᴀʏᴇɢɪ.`")


# ================================
#      PROMO COMMAND (ANU MATRIX)
# ================================
@app.on_message(filters.command(["promo"]) & SUDOERS)
async def promos(client, message: Message):
    bot_username = app.username
    
    # 🌟 Get Promo Image from Database
    db_data = await promo_db.find_one({"_id": "promo_pic"})
    final_pic = db_data["file_id"] if db_data and "file_id" in db_data else "https://files.catbox.moe/x832ly.jpg"

    # YORSA STYLE ADD BUTTON
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ ˹ ᴀ ᴅ ᴅ  ᴛ ᴏ  ʏ ᴏ ᴜ ʀ  ɢ ʀ ᴏ ᴜ ᴩ ˼", 
                url=f"https://t.me/{bot_username}?startgroup=true"
            )
        ]
    ]

    # ANU DARK THEME UI BOXES
    anu_promo = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ** 🎵\n"
        f"┠ {get_vip()} {get_vip()} {get_vip()}\n"
        f"┠ ᴛʜᴇ ᴍᴏꜱᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜꜱɪᴄ ᴇɴɢɪɴᴇ\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} **ᴡʜʏ ᴄʜᴏᴏꜱᴇ ᴀɴᴜ?**\n"
        f"┠ ⇛ ʟᴀɢ-ꜰʀᴇᴇ ɢʀᴏᴜᴩ ᴠᴄ ꜱᴛʀᴇᴀᴍɪɴɢ\n"
        f"┠ ⇛ ʜɪɢʜ-ꜰɪᴅᴇʟɪᴛʏ ᴀᴜᴅɪᴏ Qᴜᴀʟɪᴛʏ\n"
        f"┠ ⇛ 24/7 ᴜɴɪɴᴛᴇʀʀᴜᴩᴛᴇᴅ ᴜᴩᴛɪᴍᴇ\n"
        f"┠ ⇛ ᴅᴀʀᴋ & ᴩʀᴇᴍɪᴜᴍ ᴜɪ {get_vip()}\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┠ 🖤 **ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꜱʏꜱᴛᴇᴍ**"
    )

    # Sending the Promo
    await message.reply_photo(
        photo=final_pic, 
        caption=anu_promo,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
