import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "🎵 Music Bot ready!\n\n"
        "Use:\n/play <song name>"
    )

@app.on_message(filters.command("play"))
async def play(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Example: /play Arijit Singh")
        return

    query = " ".join(message.command[1:])
    await message.reply_text(f"🔎 YouTube par searching: {query}...")

    try:
        options = {
            "quiet": True,
            "extract_flat": True,
            "default_search": "ytsearch",
        }

        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(query, download=False)

        if "entries" in info and info["entries"]:
            video = info["entries"][0]
            title = video.get("title", "Unknown")
            url = video.get("url")

            await message.reply_text(
                f"🎵 Found:\n{title}\n\n{url}"
            )
        else:
            await message.reply_text("❌ Song nahi mila.")

    except Exception as e:
        await message.reply_text(f"❌ Search error: {e}")

app.run()
