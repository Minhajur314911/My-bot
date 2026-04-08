import os
import asyncio
import logging
import http.server
import socketserver
import threading
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ১. এনভায়রনমেন্ট ভেরিয়েবল লোড করা
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DATABASE_URI = os.environ.get("DATABASE_URI", "")
CHANNEL_ID = int(os.environ.get("CHANNELS", "0"))

# ২. ডাটাবেস কানেকশন (MongoDB)
db_client = AsyncIOMotorClient(DATABASE_URI)
db = db_client["movie_bot"]
movies_col = db["movies"]

# ৩. টেলিগ্রাম বট সেটআপ
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ৪. হেলথ চেক সার্ভার (Render-কে সজাগ রাখতে)
def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logger.info(f"Health check server started on port {port}")
        httpd.serve_forever()

# --- বটের ফাংশনসমূহ ---

# ক. স্টার্ট কমান্ড
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(f"হ্যালো {message.from_user.first_name}! মুভির নাম লিখে সার্চ দিন।")

# খ. অটো-ইনডেক্সিং (চ্যানেলে মুভি দিলে ডাটাবেসে সেভ হবে)
@app.on_message(filters.chat(CHANNEL_ID) & (filters.document | filters.video))
async def auto_index(client, message):
    file = message.document or message.video
    file_name = file.file_name
    file_id = file.file_id
    
    # ডাটাবেসে সেভ বা আপডেট করা
    await movies_col.update_one(
        {"file_name": file_name},
        {"$set": {"file_id": file_id, "caption": message.caption or file_name}},
        upsert=True
    )
    logger.info(f"✅ ইনডেক্স হয়েছে: {file_name}")

# গ. মুভি সার্চিং (ইউজার নাম লিখলে মুভি খুঁজে দেবে)
@app.on_message(filters.text & filters.private)
async def search_movie(client, message):
    query = message.text
    # ডাটাবেসে মুভি খোঁজা (Case-insensitive search)
    cursor = movies_col.find({"file_name": {"$regex": query, "$options": "i"}})
    results = await cursor.to_list(length=10)
    
    if results:
        for movie in results:
            await message.reply_document(
                document=movie["file_id"],
                caption=f"আপনার মুভি: {movie['file_name']}"
            )
    else:
        await message.reply_text("দুঃখিত, এই নামে কোনো মুভি খুঁজে পাওয়া যায়নি।")

# ৫. মেইন রানার
if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    logger.info("✅ বট সফলভাবে চালু হয়েছে!")
    app.run()
