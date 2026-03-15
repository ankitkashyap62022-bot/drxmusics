from pyrogram import filters
from pyrogram.types import Message

from RessoMusic import app
from RessoMusic.core.call import AMBOTOP
from RessoMusic.misc import db
from RessoMusic.utils.database import set_loop, remove_active_chat
from RessoMusic.utils.decorators import AdminRightsCheck
from RessoMusic.utils.inline import close_markup
from config import BANNED_USERS

@app.on_message(
    filters.command(["end", "stop", "cend", "cstop"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    await AMBOTOP.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    
    
    try:
        db[chat_id].clear()
    except:
        pass
    try:
        await remove_active_chat(chat_id)
    except:
        pass

    await message.reply_text(
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
        )
    
