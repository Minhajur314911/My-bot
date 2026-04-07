import os
import asyncio
import logging
from pyrogram import Client, filters

# লগিং কনফিগারেশন
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# এনভায়রনমেন্ট ভেরিয়েবল লোড
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ভেরিফিকেশন (খালি থাকলে এরর দেখাবে)
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("API_ID, API_HASH, BOT_TOKEN সেট করা হয়নি!")

# বট ক্লায়েন্ট
app = Client(
    "my_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start কমান্ড
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user = message.from_user
    name = user.first_name if user else "User"

    await message.reply_text(
        f"হ্যালো {name}!\n🤖 বটটি এখন সচল আছে।"
    )

# রান ফাংশন
async def main():
    async with app:
        print("✅ বট সফলভাবে চালু হয়েছে!")
        await asyncio.Event().wait()  # বট চালু রাখে

# এন্ট্রি পয়েন্ট
if __name__ == "__main__":
    asyncio.run(main())
