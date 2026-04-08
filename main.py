import os
import asyncio
import logging
from pyrogram import Client, filters

# ধাপ ১-৫: লগিং এবং প্রয়োজনীয় লাইব্রেরি সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ধাপ ৬-১১: এনভায়রনমেন্ট ভেরিয়েবল লোড এবং চেক
# Render-এর 'Environment' সেকশনে আপনি যে নামগুলো (Key) দিয়েছেন, এখানে সেগুলোই ব্যবহার করা হয়েছে
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

if not API_ID or not API_HASH or not BOT_TOKEN:
    logger.error("ভুল: API_ID, API_HASH অথবা BOT_TOKEN পাওয়া যায়নি!")
    # Render-এর এনভায়রনমেন্ট ভেরিয়েবল চেক করতে হবে

# ধাপ ১২: বট ক্লায়েন্ট কনফিগারেশন
app = Client(
    "my_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ধাপ ১৩: কমান্ড হ্যান্ডলার (/start কমান্ডের জন্য)
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_name = message.from_user.first_name if message.from_user else "User"
    await message.reply_text(
        f"হ্যালো {user_name}!\n\n"
        "🤖 আপনার টেলিগ্রাম বটটি এখন সফলভাবে সচল আছে।\n"
        "এটি Render এবং Python 3.10-এ রান করছে।"
    )

# ধাপ ১৪: মেইন রান ফাংশন (বটকে চালু রাখার জন্য)
async def main():
    async with app:
        logger.info("✅ বট সফলভাবে চালু হয়েছে এবং মেসেজের জন্য অপেক্ষা করছে...")
        await asyncio.Event().wait()

# ধাপ ১৫: এন্ট্রি পয়েন্ট
if __name__ == "__main__":
    try:
        # এটি পাইথনের নতুন ভার্সনগুলোর জন্য সবচেয়ে নিরাপদ পদ্ধতি
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("বট বন্ধ করা হচ্ছে...")
