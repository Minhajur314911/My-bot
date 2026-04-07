import os
import logging
import asyncio
from pyrogram import Client, filters

# এনভায়রনমেন্ট ভেরিয়েবল
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

logging.basicConfig(level=logging.INFO)

app = Client(
    "filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(f"হ্যালো {message.from_user.first_name}!\nবটটি সফলভাবে চলছে।")

async def run_bot():
    async with app:
        print("বট চলছে...")
        await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        pass
