import re
from youtubesearchpython.__future__ import VideosSearch

# 🔥 MONGODB CONNECTION FOR CUSTOM THUMBNAIL 🔥
from RessoMusic.core.mongo import mongodb
custom_thumb_db = mongodb.custom_thumb

async def get_custom_thumb():
    try:
        data = await custom_thumb_db.find_one({"_id": "custom_thumbnail"})
        return data["url"] if data else None
    except:
        return None

# 🔥 FAIL-SAFE FALLBACK IMAGE 🔥
FALLBACK_IMG = "https://telegra.ph/file/82b13eddfc5eb944b76e2.jpg"

async def get_thumb(videoid: str) -> str:
    # 👑 1. DIRECT CUSTOM URL RETURN (ULTRA FAST - 0.01s)
    custom_url = await get_custom_thumb()
    if custom_url:
        return custom_url # No downloading, no editing, direct link!

    # 👑 2. YOUTUBE DEFAULT (IF CUSTOM NOT SET)
    if not videoid or not re.match(r"^[a-zA-Z0-9_-]{11}$", videoid):
        return FALLBACK_IMG

    try:
        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]
        thumb = result.get("thumbnails", [{}])[0].get("url", "").split("?")[0]
        return thumb if thumb else FALLBACK_IMG
    except Exception:
        return FALLBACK_IMG

# ========================
# Backward Compatibility
# ========================
gen_thumb = get_thumb
