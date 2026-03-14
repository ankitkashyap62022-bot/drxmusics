import aiohttp
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔥 IMPORTING MAIN APP FROM YOUR MUSIC BOT CONFIG 🔥
from RessoMusic import app 

# 🔗 YOUR SUPPORT BUTTON
support_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton("📢 Support Channel", url="https://t.me/FUCK_BY_REFLEX")]]
)

# ================================
#        NUMBER SEARCH COMMAND
# ================================
@app.on_message(filters.command(["num", "osint", "trace", "track"]))
async def search(client, message):
    
    # Check if user provided a number with the command
    if len(message.command) < 2:
        text = """
👁 **Madara OSINT Bot**

📱 Send any mobile number with the command to get information.

**Example:**
`/num 9876543210`
"""
        return await message.reply_text(text, reply_markup=support_button)

    number = message.command[1].strip()

    if not number.isdigit() or len(number) < 10:
        return await message.reply_text("❌ **Send valid 10-digit mobile number!**")

    # ⏳ Processing Message
    msg = await message.reply_text("⏳ **Fetching details, please wait...**")

    # 🔥 DUAL API SETUP (Anti-Crash System)
    url_1 = f"https://openosintx.vippanel.in/num.php?key=ee60289a7e31e88bd0d9e9fdcfb25e11&number={number}"
    url_2 = f"https://ashuapi.ashupanel.online/api/gateway.php?key=sevenday&number={number}"

    data = None

    try:
        async with aiohttp.ClientSession() as session:
            # 👑 TRY API 1 (Main)
            async with session.get(url_1, timeout=10) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                    except Exception:
                        pass
            
            # 👑 FALLBACK TO API 2 (If API 1 gives 500 Error or fails)
            if not data:
                async with session.get(url_2, timeout=10) as response2:
                    if response2.status == 200:
                        try:
                            data = await response2.json()
                        except Exception:
                            pass

    except Exception:
        return await msg.edit_text("⚠️ **Critical Error.** Both APIs are down right now.")

    # If both APIs returned nothing
    if not data:
        return await msg.edit_text("⚠️ **API Error.** Server didn't respond with valid data.")

    # 🔎 PARSING AND FORMATTING RESULTS
    result = "🔎 **Madara OSINT Result**\n\n"
    found = False

    if isinstance(data, dict):
        for key, info in data.items():
            if isinstance(info, dict):
                found = True
                # Extracting values safely
                name = info.get("NAME") or info.get("name", "N/A")
                father = info.get("fname") or info.get("FATHER", "N/A")
                address = info.get("ADDRESS") or info.get("address", "N/A")
                circle = info.get("circle") or info.get("CIRCLE", "N/A")
                email = info.get("EMAIL") or info.get("email", "N/A")

                # Fixed Markdown Formatting
                result += f"👤 **Name:** `{name}`\n"
                result += f"👨 **Father:** `{father}`\n"
                result += f"📍 **Address:** `{address}`\n"
                result += f"📡 **Circle:** `{circle}`\n"
                result += f"📧 **Email:** `{email}`\n"
                result += "━━━━━━━━━━━━━━\n"
            elif isinstance(info, (str, int)) and str(info).strip() != "":
                # Fallback if data is flat
                found = True
                result += f"┠ ⇛ **{str(key).upper()}:** `{info}`\n"

    if not found:
        result = "❌ **No data found for this number in the database.**"

    # Send Final Result
    await msg.edit_text(result, reply_markup=support_button)
