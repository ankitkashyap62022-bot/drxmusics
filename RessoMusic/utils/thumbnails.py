import asyncio, os, re, httpx
from io import BytesIO
from PIL import Image, ImageEnhance
from aiofiles.os import path as aiopath

from ..logging import LOGGER
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

FALLBACK_IMAGE_PATH = "RessoMusic/assets/controller.png"
YOUTUBE_IMG_URL = "https://i.ytimg.com/vi/default.jpg"

# ========================
# Utilities (Ultra Fast Resize)
# ========================
async def resize_youtube_thumbnail(img: Image.Image) -> Image.Image:
    target_width, target_height = 1280, 720
    aspect_ratio = img.width / img.height
    target_ratio = target_width / target_height

    if aspect_ratio > target_ratio:
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    cropped = img.crop((left, top, right, bottom))
    
    # 💎 Premium Look (Thoda Color & Sharpness badha diya)
    enhanced = ImageEnhance.Sharpness(cropped).enhance(1.5)
    enhanced = ImageEnhance.Color(enhanced).enhance(1.2)
    return enhanced

async def fetch_image(url: str) -> Image.Image:
    async with httpx.AsyncClient() as client:
        try:
            if not url:
                raise ValueError("No thumbnail URL provided")
            response = await client.get(url, timeout=5)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img = await resize_youtube_thumbnail(img)
            return img
        except Exception as e:
            LOGGER.error("Image loading error for URL %s: %s", url, e)
            try:
                response = await client.get(YOUTUBE_IMG_URL, timeout=5)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img = await resize_youtube_thumbnail(img)
                return img
            except Exception:
                # 🖤 Emergency Black Image (Agar sab fail ho jaye)
                return Image.new("RGB", (1280, 720), (20, 20, 20))

# ========================
# Main Function
# ========================
async def get_thumb(videoid: str) -> str:
    if not videoid or not re.match(r"^[a-zA-Z0-9_-]{11}$", videoid):
        return ""

    save_dir = f"database/photos/{videoid}.png"

    try:
        save_dir_parent = "database/photos"
        if not await aiopath.exists(save_dir_parent):
            await asyncio.to_thread(os.makedirs, save_dir_parent)
    except Exception:
        return ""

    # 👑 CHECK MONGODB FOR ANU'S CUSTOM THUMBNAIL
    custom_url = await get_custom_thumb()

    if custom_url:
        thumbnail_url = custom_url
    else:
        try:
            url = f"https://www.youtube.com/watch?v={videoid}"
            results = VideosSearch(url, limit=1)
            result = (await results.next())["result"][0]
            thumbnail_url = result.get("thumbnails", [{}])[0].get("url", "").split("?")[0]
        except Exception:
            thumbnail_url = YOUTUBE_IMG_URL

    # 🔥 GENERATE PURE, SMOOTH & TEXT-FREE IMAGE
    img = await fetch_image(thumbnail_url)

    try:
        await asyncio.to_thread(img.save, save_dir, format="PNG", quality=95, optimize=True)
        img.close()
        if await aiopath.exists(save_dir):
            return save_dir
    except Exception as e:
        LOGGER.error("Thumbnail save error for %s: %s", save_dir, e)
        img.close()

    return ""

gen_thumb = get_thumb
