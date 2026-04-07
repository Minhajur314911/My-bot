import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# আপনার এনভায়রনমেন্ট ভেরিয়েবলগুলো
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# বট ক্লায়েন্ট সেটআপ
app = Client(
    "filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# /start কমান্ড
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        f"হ্যালো {message.from_user.mention}!\nআমি একটি অটো ফিল্টার বট। "
        "চ্যানেলে ফাইল থাকলে আমি আপনাকে তা খুঁজে দেব।",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("আমাদের চ্যানেল", url="https://t.me/your_channel")]]
        )
    )

# অটো ফিল্টার লজিক (আপনার ডাটাবেজ অনুযায়ী কাজ করবে)
@app.on_message(filters.text & filters.group)
async def filter_logic(client, message):
    query = message.text.lower()
    # এখানে আমরা চাইলে আপনার মুভি বা ফাইলের নাম সার্চ করার লজিক বসাতে পারি
    if "hello" in query:
        await message.reply_text("হ্যালো! আমি আপনাকে কীভাবে সাহায্য করতে পারি?")

print("বটটি সফলভাবে চালু হয়েছে!")
app.run()
