import re
import time
import logging
from youtubesearchpython.__future__ import VideosSearch
from RessoMusic.core.mongo import mongodb

# 👑 LOGGING SETUP (To catch silent errors) 👑
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("RessoMusic.Thumbnails")

# 🔥 MONGODB CONNECTION FOR CUSTOM THUMBNAIL 🔥
custom_thumb_db = mongodb.custom_thumb

# 🔥 SAFE FALLBACK IMAGE (Anti-Crash Guard) 🔥
FALLBACK_IMG = "https://telegra.ph/file/82b13eddfc5eb944b76e2.jpg"

# 🚀 IN-MEMORY CACHE FOR ULTRA-FAST PERFORMANCE 🚀
# (Ye baar-baar database ko spam nahi karega, bot ko superfast banayega!)
_CACHE = {"url": None, "time": 0}
CACHE_TTL = 180  # 3 minutes cache refresh time

async def get_custom_thumb():
    """ Fetches custom thumbnail from DB with Caching mechanism """
    current_time = time.time()
    
    # ⚡ Cache Hit: Return immediately without touching Database
    if _CACHE["url"] and (current_time - _CACHE["time"]) < CACHE_TTL:
        return _CACHE["url"]

    # ⚡ Cache Miss: Fetch from MongoDB & Update Cache
    try:
        data = await custom_thumb_db.find_one({"_id": "custom_thumbnail"})
        if data and "url" in data:
            _CACHE["url"] = data["url"]
            _CACHE["time"] = current_time
            return data["url"]
    except Exception as e:
        LOGGER.error(f"⚠️ [DB ERROR] Failed to fetch custom thumb: {e}")
        
    return None

async def get_thumb(videoid: str) -> str:
    """ The Ultimate Thumbnail Generator (Custom -> YouTube -> Fallback) """
    
    # 👑 PRIORITY 1: DIRECT CUSTOM URL RETURN (0.01s Execution)
    custom_url = await get_custom_thumb()
    if custom_url:
        return custom_url # 😈 Seedha teri photo jayegi!

    # 👑 PRIORITY 2: YOUTUBE DEFAULT (Agar /setply set nahi hai)
    if not videoid or not re.match(r"^[a-zA-Z0-9_-]{11}$", videoid):
        return FALLBACK_IMG

    try:
        # Optimized YouTube API Call
        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)
        result = await results.next()
        
        # Safe Extraction of 4K Image Link
        if result and "result" in result and len(result["result"]) > 0:
            thumb = result["result"][0].get("thumbnails", [{}])[0].get("url", "")
            clean_thumb = thumb.split("?")[0] # Removes garbage queries for clean image
            return clean_thumb if clean_thumb else FALLBACK_IMG
            
    except Exception as e:
        LOGGER.error(f"⚠️ [YT ERROR] Thumbnail fetch failed for {videoid}: {e}")
        return FALLBACK_IMG

    return FALLBACK_IMG

# ========================
# Backward Compatibility
# ========================
gen_thumb = get_thumb
