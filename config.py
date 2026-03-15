import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# 👑 THE ANU MATRIX CREDENTIALS
API_ID = int(getenv("API_ID", 22002688))
API_HASH = getenv("API_HASH", "0c3bee507e2ea7621b903b12ef11fba9")

# 🤖 BOT TOKEN (Hidden securely)
BOT_TOKEN = getenv("BOT_TOKEN", "8430966075:AAH8fOGA2CCZYiq8v4YuvYVmsg8XL-2KTPM")

# 🗄️ MONGO DB (With Custom Database Name to avoid clash with Userbot)
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://Billa:ZARA838180@billa.0srztoh.mongodb.net/ZARA_HACK_BOT?retryWrites=true&w=majority")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 600))

# Chat id of a group for logging bot's activities 
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", -1003201139840))

# 👑 SUPREME COMMANDER ID
OWNER_ID = int(getenv("OWNER_ID", 7580691483))

## Fill these variables if you're deploying on heroku.
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ⚙️ Auto-Update Repo
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/hkmusic/drxmusic",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", "")  

# 🚫 PROMOTION LINKS REMOVED (Ab button aayenge 100%)
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/MONSTER_FUCK_BITCHES")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/FUCK_BY_REFLEX")


# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# make your bots privacy from telegra.ph and put your url here 
PRIVACY_LINK = getenv("PRIVACY_LINK", "https://files.catbox.moe/jyeumn.jpg")

# Music Api
API_URL = getenv("API_URL", 'https://api.thequickearn.xyz') 
VIDEO_API_URL = getenv("VIDEO_API_URL", 'https://api.video.thequickearn.xyz')
API_KEY = getenv("API_KEY", None)

# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))

# 🎧 THE PYROGRAM V2 STRING SESSION (Assistant Id)
STRING1 = getenv("STRING_SESSION", "BQImFsUAwF9UPKoiu__sc8bT-QGgNSWJYjz5GVYV90Lz0NIxFGERUttPh7xFmCN5RyQgPcnXlsZl8_2o6g0jmk9pA4fDh6P2b20PFkQRY-6rE7jGt5Y6_OiMZ99DjAe484LFLrPP6ka46dmCl_WhZdOQSrTAQyyZ8fiq7EK1MmXYHaMWW73gFCqbJA67v8Vs9IVxS9h8t5Jd1lZ3cMCOCcVmECiSIEnccRSCW2eIQZG4TT-ydau1QWGgzlTfHWbiUC0zeG6IQgb4cgJdaR-j-nbZBLT2_Uzho6Wj9D_PwQRsimAio7GtztNTSkn1Usw9zi0d08Bfe3id00v1ggM4oEgTQ-LsmQAAAAHutjURAA")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# 🔥 SAFE FALLBACKS (Teri Custom Photo Yaha Set Hai!)
FALLBACK_IMG = "https://files.catbox.moe/s8bo2x.jpg"

# 🎨 BRANDING IMAGES (Sab jagah teri photo override karegi)
START_IMG_URL = getenv("START_IMG_URL", FALLBACK_IMG)
PING_IMG_URL = getenv("PING_IMG_URL", FALLBACK_IMG)
PLAYLIST_IMG_URL = FALLBACK_IMG
STATS_IMG_URL = FALLBACK_IMG

TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", FALLBACK_IMG)
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", FALLBACK_IMG)
STREAM_IMG_URL = getenv("STREAM_IMG_URL", FALLBACK_IMG)
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", FALLBACK_IMG)
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", FALLBACK_IMG)
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", FALLBACK_IMG)
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", FALLBACK_IMG)
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", FALLBACK_IMG)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
        )
