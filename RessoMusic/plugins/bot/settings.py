import random
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from RessoMusic import app
from RessoMusic.utils.database import (
    add_nonadmin_chat,
    get_authuser,
    get_authuser_names,
    get_playmode,
    get_playtype,
    get_upvote_count,
    is_nonadmin_chat,
    is_skipmode,
    remove_nonadmin_chat,
    set_playmode,
    set_playtype,
    set_upvotes,
    skip_off,
    skip_on,
)
# bot_sys_stats removed from below to fix lag
from RessoMusic.utils.decorators.admins import ActualAdminCB
from RessoMusic.utils.decorators.language import language, languageCB
from RessoMusic.utils.inline.settings import (
    auth_users_markup,
    playmode_users_markup,
    setting_markup,
    vote_mode_markup,
)
from config import BANNED_USERS, OWNER_ID

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

# YORSA STYLE PRIVATE PANEL BUTTONS (NO EID ERROR IN BUTTONS)
def anu_private_panel(bot_username):
    return [
        [
            InlineKeyboardButton(text="↪ ˹ ᴛ ᴀ ᴩ  ᴛ ᴏ  ꜱ ᴇ ᴇ  ᴍ ᴀ ɢ ɪ ᴄ ˼ ↩", url=f"https://t.me/{bot_username}?startgroup=true")
        ],
        [
            InlineKeyboardButton(text="💬 ˹ ꜱ ᴜ ᴩ ᴩ ᴏ ʀ ᴛ ˼", url="https://t.me/BMW_USERBOT_II"),
            InlineKeyboardButton(text="🐱 ˹ ᴍ ʏ  ʜ ᴏ ᴍ ᴇ ˼", url="https://t.me/FUCK_BY_REFLEX")
        ],
        [
            InlineKeyboardButton(text="🤷‍♂️ ˹ ʜ ᴇ ʟ ᴩ  ᴀ ɴ ᴅ  ᴄ ᴏ ᴍ ᴍ ᴀ ɴ ᴅ ꜱ ˼", callback_data="anu_help_menu")
        ],
        [
            InlineKeyboardButton(text="🕶 ˹ ᴍ ʏ  ᴍ ᴀ ꜱ ᴛ ᴇ ʀ 👑 ˼", url="https://t.me/MONSTER_FUCK_BITCHES")
        ]
    ]

# ================================
#      /SETTINGS COMMAND
# ================================
@app.on_message(
    filters.command(["settings", "setting"]) & filters.group & ~BANNED_USERS
)
@language
async def settings_mar(client, message: Message, _):
    buttons = setting_markup(_)
    anu_settings = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} **ᴀɴᴜ ꜱᴇᴛᴛɪɴɢꜱ ᴍᴀɪɴꜰʀᴀᴍᴇ**\n"
        f"┠ {get_vip()} {get_vip()} {get_vip()}\n"
        f"┠ ɢʀᴏᴜᴩ: {message.chat.title}\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} ᴄᴏɴꜰɪɢᴜʀᴇ ᴀɴᴜ ᴍᴀᴛʀɪx:\n"
        f"┠ ⇛ ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ\n"
        f"┠ ⇛ ᴄᴜꜱᴛᴏᴍɪᴢᴇ ᴩʟᴀʏᴍᴏᴅᴇ, ᴀᴜᴛʜ\n"
        f"┠ ⇛ ᴜꜱᴇʀꜱ ᴀɴᴅ ᴠᴏᴛᴇ-ꜱᴋɪᴩ ᴍᴏᴅᴇꜱ.\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┠ 🖤 **ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꜱʏꜱᴛᴇᴍ**"
    )
    await message.reply_text(
        anu_settings,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settings_helper") & ~BANNED_USERS)
@languageCB
async def settings_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer(_["set_cb_5"])
    except:
        pass
    buttons = setting_markup(_)

    anu_settings = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} **ᴀɴᴜ ꜱᴇᴛᴛɪɴɢꜱ ᴍᴀɪɴꜰʀᴀᴍᴇ**\n"
        f"┠ {get_vip()} {get_vip()} {get_vip()}\n"
        f"┠ ɢʀᴏᴜᴩ: {CallbackQuery.message.chat.title}\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┠ {get_vip()} ᴄᴏɴꜰɪɢᴜʀᴇ ᴀɴᴜ ᴍᴀᴛʀɪx:\n"
        f"┠ ⇛ ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ\n"
        f"┠ ⇛ ᴄᴜꜱᴛᴏᴍɪᴢᴇ ᴩʟᴀʏᴍᴏᴅᴇ, ᴀᴜᴛʜ\n"
        f"┠ ⇛ ᴜꜱᴇʀꜱ ᴀɴᴅ ᴠᴏᴛᴇ-ꜱᴋɪᴩ ᴍᴏᴅᴇꜱ.\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"┠ 🖤 **ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꜱʏꜱᴛᴇᴍ**"
    )
    return await CallbackQuery.edit_message_text(
        anu_settings,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_markup(client, CallbackQuery: CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    if CallbackQuery.message.chat.type == ChatType.PRIVATE:
        # THE CRASH FIX: bot_sys_stats removed to make buttons FAST & SMOOTH!
        bot_username = app.username
        buttons = anu_private_panel(bot_username)

        caption = (
            f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"┠ {get_vip()} ʜ ᴇ ʏ ,  {CallbackQuery.from_user.mention}\n"
            f"┠ {get_vip()} {get_vip()} {get_vip()}\n"
            f"┠ {get_vip()} ɪ ᴀᴍ ᴀɴᴜ ᴍᴀᴛʀɪx 🎵\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"┠ {get_vip()} ɪ ᴀᴍ ᴛʜᴇ ꜰᴀꜱᴛᴇꜱᴛ ᴀɴᴅ ᴩᴏᴡᴇʀꜰᴜʟ\n"
            f"┠ ᴍᴜꜱɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ\n"
            f"┠ ꜱᴏᴍᴇ ᴀᴡᴇꜱᴏᴍᴇ ꜰᴇᴀᴛᴜʀᴇꜱ {get_vip()}\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"┠ 🖤 ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꜱʏꜱᴛᴇᴍ {get_vip()}\n"
        )
        return await CallbackQuery.edit_message_caption(
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = setting_markup(_)
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|ANSWERVOMODE|VOTEANSWER|PM|AU|VM)$"
    )
    & ~BANNED_USERS
)
@languageCB
async def without_Admin_rights(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "SEARCHANSWER":
        try:
            return await CallbackQuery.answer(_["setting_2"], show_alert=True)
        except:
            return
    if command == "PLAYMODEANSWER":
        try:
            return await CallbackQuery.answer(_["setting_5"], show_alert=True)
        except:
            return
    if command == "PLAYTYPEANSWER":
        try:
            return await CallbackQuery.answer(_["setting_6"], show_alert=True)
        except:
            return
    if command == "AUTHANSWER":
        try:
            return await CallbackQuery.answer(_["setting_3"], show_alert=True)
        except:
            return
    if command == "VOTEANSWER":
        try:
            return await CallbackQuery.answer(
                _["setting_8"],
                show_alert=True,
            )
        except:
            return
    if command == "ANSWERVOMODE":
        current = await get_upvote_count(CallbackQuery.message.chat.id)
        try:
            return await CallbackQuery.answer(
                _["setting_9"].format(current),
                show_alert=True,
            )
        except:
            return
    if command == "PM":
        try:
            await CallbackQuery.answer(_["set_cb_2"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "AU":
        try:
            await CallbackQuery.answer(_["set_cb_1"], show_alert=True)
        except:
            pass
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            buttons = auth_users_markup(_, True)
        else:
            buttons = auth_users_markup(_)
    if command == "VM":
        mode = await is_skipmode(CallbackQuery.message.chat.id)
        current = await get_upvote_count(CallbackQuery.message.chat.id)
        buttons = vote_mode_markup(_, current, mode)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex("FERRARIUDTI") & ~BANNED_USERS)
@ActualAdminCB
async def addition(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    mode = callback_data.split(None, 1)[1]
    if not await is_skipmode(CallbackQuery.message.chat.id):
        return await CallbackQuery.answer(_["setting_10"], show_alert=True)
    current = await get_upvote_count(CallbackQuery.message.chat.id)
    if mode == "M":
        final = current - 2
        print(final)
        if final == 0:
            return await CallbackQuery.answer(
                _["setting_11"],
                show_alert=True,
            )
        if final <= 2:
            final = 2
        await set_upvotes(CallbackQuery.message.chat.id, final)
    else:
        final = current + 2
        print(final)
        if final == 17:
            return await CallbackQuery.answer(
                _["setting_12"],
                show_alert=True,
            )
        if final >= 15:
            final = 15
        await set_upvotes(CallbackQuery.message.chat.id, final)
    buttons = vote_mode_markup(_, final, True)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(
    filters.regex(pattern=r"^(MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$")
    & ~BANNED_USERS
)
@ActualAdminCB
async def playmode_ans(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "CHANNELMODECHANGE":
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = None
        else:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = True
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "MODECHANGE":
        try:
            await CallbackQuery.answer(_["set_cb_3"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            await set_playmode(CallbackQuery.message.chat.id, "Inline")
            Direct = None
        else:
            await set_playmode(CallbackQuery.message.chat.id, "Direct")
            Direct = True
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = False
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "PLAYTYPECHANGE":
        try:
            await CallbackQuery.answer(_["set_cb_3"], show_alert=True)
        except:
            pass
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            await set_playtype(CallbackQuery.message.chat.id, "Admin")
            Playtype = False
        else:
            await set_playtype(CallbackQuery.message.chat.id, "Everyone")
            Playtype = True
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex(pattern=r"^(AUTH|AUTHLIST)$") & ~BANNED_USERS)
@ActualAdminCB
async def authusers_mar(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "AUTHLIST":
        _authusers = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _authusers:
            try:
                return await CallbackQuery.answer(_["setting_4"], show_alert=True)
            except:
                return
        else:
            try:
                await CallbackQuery.answer(_["set_cb_4"], show_alert=True)
            except:
                pass
            j = 0

            # ANU DARK THEME AUTH LIST
            msg = (
                f"┏━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"┠ {get_vip()} **ᴀɴᴜ ᴀᴜᴛʜ ʟɪꜱᴛ**\n"
                f"┠ {get_vip()} {get_vip()} {get_vip()}\n"
                f"┠ ɢʀᴏᴜᴩ: {CallbackQuery.message.chat.title}\n"
                f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )

            for note in _authusers:
                _note = await get_authuser(CallbackQuery.message.chat.id, note)
                user_id = _note["auth_user_id"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name
                    j += 1
                except:
                    continue
                msg += f"┠ ⇛ **{j}** ➤ {user} [`{user_id}`]\n"
                msg += f"┠ ⇛ ᴀᴅᴅᴇᴅ ʙʏ: {admin_name}\n"

            msg += f"┗━━━━━━━━━━━━━━━━━━━━━━━━\n\n┠ 🖤 **ᴩᴏᴡᴇʀᴇᴅ ʙʏ » ᴀɴᴜ ꜱʏꜱᴛᴇᴍ**"

            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔙 ˹ ʙ ᴀ ᴄ ᴋ ˼", callback_data=f"AU"
                        ),
                        InlineKeyboardButton(
                            text="❌ ˹ ᴄ ʟ ᴏ ꜱ ᴇ ˼",
                            callback_data=f"close",
                        ),
                    ]
                ]
            )
            try:
                return await CallbackQuery.edit_message_text(msg, reply_markup=upl)
            except MessageNotModified:
                return
    try:
        await CallbackQuery.answer(_["set_cb_3"], show_alert=True)
    except:
        pass
    if command == "AUTH":
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            buttons = auth_users_markup(_)
        else:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            buttons = auth_users_markup(_, True)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex("VOMODECHANGE") & ~BANNED_USERS)
@ActualAdminCB
async def vote_change(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    try:
        await CallbackQuery.answer(_["set_cb_3"], show_alert=True)
    except:
        pass
    mod = None
    if await is_skipmode(CallbackQuery.message.chat.id):
        await skip_off(CallbackQuery.message.chat.id)
    else:
        mod = True
        await skip_on(CallbackQuery.message.chat.id)
    current = await get_upvote_count(CallbackQuery.message.chat.id)
    buttons = vote_mode_markup(_, current, mod)

    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return
