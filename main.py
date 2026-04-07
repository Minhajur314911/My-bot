import os
import asyncio
import logging
from pyrogram import Client, filters

# এনভায়রনমেন্ট ভেরিয়েবলগুলো নিচ্ছি
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# বট ক্লায়েন্ট সরাসরি ডিফাইন করা
app = Client(
    "my_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start কমান্ড লজিক
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text(f"হ্যালো {message.from_user.first_name}!\nবটটি এখন সচল আছে।")

# অটো ফিল্টার লজিক
@app.on_message(filters.text & filters.group)
async def group_filter(client, message):
    if "hello" in message.text.lower():
        await message.reply_text("হ্যালো! আমি আপনাকে কীভাবে সাহায্য করতে পারি?")

# রান করার আধুনিক পদ্ধতি
if __name__ == "__main__":
    print("বটটি সফলভাবে চালু হচ্ছে...")
    app.run()
