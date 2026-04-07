import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# এনভায়রনমেন্ট ভেরিয়েবল
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

async def main():
    app = Client(
        "filter_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

    @app.on_message(filters.command("start") & filters.private)
    async def start(client, message):
        await message.reply_text(
            f"হ্যালো {message.from_user.mention}!\nআমি একটি অটো ফিল্টার বট।",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("আমাদের চ্যানেল", url="https://t.me/your_channel")]]
            )
        )

    @app.on_message(filters.text & filters.group)
    async def filter_logic(client, message):
        if "hello" in message.text.lower():
            await message.reply_text("হ্যালো! আমি আপনাকে কীভাবে সাহায্য করতে পারি?")

    print("বটটি সফলভাবে চালু হয়েছে!")
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
