import random
from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from RessoMusic import app
from RessoMusic.utils import help_pannel
from RessoMusic.utils.database import get_lang
from RessoMusic.utils.decorators.language import LanguageStart, languageCB
from RessoMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, SUPPORT_GROUP
from strings import get_string, helpers
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
#        /HELP COMMAND (DM)
# ================================
@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)
    
    # 🌟 YORSA BOX UI FOR HELP MENU
    anu_help_caption = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} **ᴀɴᴜ ᴄᴏᴍᴍᴀɴᴅ ᴍᴀɪɴꜰʀᴀᴍᴇ**\n"
        f"┠ {get_vip()} {get_vip()} {get_vip()}\n"
        f"┠ ᴄʜᴏᴏꜱᴇ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} ɴᴇᴇᴅ ᴀꜱꜱɪꜱᴛᴀɴᴄᴇ?\n"
        f"┠ ᴊᴏɪɴ ᴏᴜʀ ꜱᴜᴩᴩᴏʀᴛ ɢʀᴏᴜᴩ ꜰᴏʀ ʜᴇʟᴩ.\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┠ 🖤 **ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꜱʏꜱᴛᴇᴍ**"
    )

    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        
        await update.edit_message_caption(
            caption=anu_help_caption, reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        final_pic = await get_start_image() # Dynamic Pic from DB
        
        await update.reply_photo(
            photo=final_pic,
            caption=anu_help_caption,
            reply_markup=keyboard,
        )

# ================================
#      /HELP COMMAND (GROUP)
# ================================
@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    
    anu_grp_help = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ**\n"
        f"┠ ⇛ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ꜱᴇᴇ\n"
        f"┠ ⇛ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ.\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await message.reply_text(anu_grp_help, reply_markup=InlineKeyboardMarkup(keyboard))

# ================================
#      INLINE CALLBACKS (PAGES)
# ================================
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)
    
    # Adding ANU Header to all Help Pages
    anu_header = f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n┠ {get_vip()} **ᴀɴᴜ ʜᴇʟᴩ ᴍᴀɪɴꜰʀᴀᴍᴇ**\n┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if cb == "hb1":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_1, reply_markup=keyboard)
    elif cb == "hb2":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_2, reply_markup=keyboard)
    elif cb == "hb3":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_3, reply_markup=keyboard)
    elif cb == "hb4":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_4, reply_markup=keyboard)
    elif cb == "hb5":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_5, reply_markup=keyboard)
    elif cb == "hb6":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_6, reply_markup=keyboard)
    elif cb == "hb7":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_7, reply_markup=keyboard)
    elif cb == "hb8":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_8, reply_markup=keyboard)
    elif cb == "hb9":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_9, reply_markup=keyboard)
    elif cb == "hb10":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_10, reply_markup=keyboard)
    elif cb == "hb11":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_11, reply_markup=keyboard)
    elif cb == "hb12":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_12, reply_markup=keyboard)
    elif cb == "hb13":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_13, reply_markup=keyboard)
    elif cb == "hb14":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_14, reply_markup=keyboard)
    elif cb == "hb15":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_15, reply_markup=keyboard)
    elif cb == "hb16":
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_16, reply_markup=keyboard)
    elif cb == "hb17":
        if CallbackQuery.from_user.id not in SUDOERS:
            await CallbackQuery.answer(f"⚠️ [ ꜱʏꜱᴛᴇᴍ ᴀʟᴇʀᴛ ]\n\nᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ! ᴛʜɪꜱ ᴩᴀɴᴇʟ ɪꜱ ᴏɴʟʏ ꜰᴏʀ ᴀɴᴜ ᴍᴀꜱᴛᴇʀꜱ (ꜱᴜᴅᴏᴇʀꜱ).", show_alert=True)
            return
        await CallbackQuery.edit_message_caption(caption=anu_header + helpers.HELP_17, reply_markup=keyboard)
