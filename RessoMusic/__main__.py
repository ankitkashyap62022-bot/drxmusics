import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from RessoMusic import LOGGER, app, userbot
from RessoMusic.core.call import AMBOTOP
from RessoMusic.misc import sudo
from RessoMusic.plugins import ALL_MODULES
from RessoMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# ☠️ ADVANCED ASCII ART FOR MONSTER ☠️
MONSTER_BANNER = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
███╗   ███╗ ██████╗ ███╗   ██╗███████╗████████╗███████╗██████╗ 
████╗ ████║██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██╔████╔██║██║   ██║██╔██╗ ██║███████╗   ██║   █████╗  ██████╔╝
██║╚██╔╝██║██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██║ ╚═╝ ██║╚██████╔╝██║ ╚████║███████║   ██║   ███████╗██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
     [ ☠️ 𝗥𝗘𝗙𝗟𝗘𝗫 𝗫 𝗦𝗬𝗦𝗧𝗘𝗠 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘𝗗 ☠️ ]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("⚠️ [CRITICAL] 𝗦𝘁𝗿𝗶𝗻𝗴 𝗦𝗲𝘀𝘀𝗶𝗼𝗻 𝗠𝗶𝘀𝘀𝗶𝗻𝗴! 𝗕𝗼𝘁 𝗖𝗮𝗻𝗻𝗼𝘁 𝗕𝗼𝗼𝘁.")
        exit()
        
    await sudo()
    
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
        
    await app.start()
    
    for all_module in ALL_MODULES:
        importlib.import_module("RessoMusic.plugins" + all_module)
        
    LOGGER("RessoMusic.plugins").info("✅ 𝗔𝗹𝗹 𝗥𝗲𝗳𝗹𝗲𝘅 𝗠𝗼𝗱𝘂𝗹𝗲𝘀 𝗜𝗻𝗷𝗲𝗰𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗕𝗮𝗯𝘆 😈...")
    
    await userbot.start()
    await AMBOTOP.start()
    
    try:
        await AMBOTOP.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("RessoMusic").error(
            "❌ [𝗙𝗔𝗧𝗔𝗟 𝗘𝗥𝗥𝗢𝗥] 𝗟𝗼𝗴 𝗚𝗿𝗼𝘂𝗽 𝗩𝗼𝗶𝗰𝗲𝗖𝗵𝗮𝘁 𝗶𝘀 𝗢𝗙𝗙𝗟𝗜𝗡𝗘!\n\n⚠️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝘁𝗮𝗿𝘁 𝗩𝗖 𝗶𝗻 𝗟𝗼𝗴 𝗚𝗿𝗼𝘂𝗽... 𝗠𝗼𝗻𝘀𝘁𝗲𝗿 𝗦𝘆𝘀𝘁𝗲𝗺 𝗦𝘁𝗼𝗽𝗽𝗶𝗻𝗴."
        )
        exit()
    except:
        pass
        
    await AMBOTOP.decorators()
    
    # 🔥 THE MONSTER BANNER PRINTING 🔥
    LOGGER("RessoMusic").info(MONSTER_BANNER)
    LOGGER("RessoMusic").info("🚀 𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗜𝗦 𝗡𝗢𝗪 𝗟𝗜𝗩𝗘 & 𝗥𝗘𝗔𝗗𝗬 𝗧𝗢 𝗙*𝗖𝗞!")
    
    await idle()
    
    # 🛑 SHUTDOWN SEQUENCE
    await app.stop()
    await userbot.stop()
    LOGGER("RessoMusic").info("⚠️ 𝗦𝗬𝗦𝗧𝗘𝗠 𝗦𝗛𝗨𝗧𝗗𝗢𝗪𝗡... 𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗞𝗘𝗥𝗡𝗘𝗟 𝗢𝗙𝗙𝗟𝗜𝗡𝗘. ☠️")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
