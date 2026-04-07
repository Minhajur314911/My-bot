import os
import asyncio
import logging
from pyrogram import Client, filters
# লগিং কনফিগারেশন
logging.basicConfig(level=logging.INFO)
# এনভায়রনমেন্ট ভেরিয়েবল চেক
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
# বট ক্লায়েন্ট সেটআপ
app = Client(
    "my_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text(f"হ্যালো {message.from_user.first_name}!\nবটটি এখন সচল আছে।")
async def main():
    await app.start()
    print("বট সফলভাবে চালু হয়েছে!")
    await asyncio.Event().wait()
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
