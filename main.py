import os, asyncio, logging, http.server, socketserver, threading
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ১. সেটিংস (Render Environment থেকে নেবে)
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DATABASE_URI = os.environ.get("DATABASE_URI", "")
CHANNEL_ID = int(os.environ.get("CHANNELS", "0"))

# ২. ডাটাবেস কানেকশন
db_client = AsyncIOMotorClient(DATABASE_URI)
db = db_client["movie_bot"]
movies_col = db["movies"]

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ৩. হেলথ চেক সার্ভার (Render-কে সজাগ রাখতে)
def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logger.info(f"Health server on port {port}")
        httpd.serve_forever()

# ৪. অটো-ইনডেক্সিং ফাংশন (বিরতিসহ যাতে ব্লক না হয়)
async def auto_index_all_movies():
    logger.info("পুরনো মুভি ইনডেক্স করা শুরু হচ্ছে...")
    count = 0
    async for msg in app.get_chat_history(CHANNEL_ID):
        if msg.document or msg.video:
            file = msg.document or msg.video
            await movies_col.update_one(
                {"file_name": file.file_name},
                {"$set": {"file_id": file.file_id, "caption": msg.caption or file.file_name}},
                upsert=True
            )
            count += 1
            # প্রতি ১০টি ফাইল ইনডেক্স করার পর ২ সেকেন্ড বিরতি
            if count % 10 == 0:
                await asyncio.sleep(2) 
                
    logger.info(f"✅ মোট {count}টি পুরনো মুভি ইনডেক্স করা হয়েছে!")

# ৫. নতুন মুভি ইনডেক্সিং (এখন থেকে যা আপলোড করবেন)
@app.on_message(filters.chat(CHANNEL_ID) & (filters.document | filters.video))
async def new_movie_index(client, message):
    file = message.document or message.video
    await movies_col.update_one(
        {"file_name": file.file_name},
        {"$set": {"file_id": file.file_id, "caption": message.caption or file.file_name}},
                upsert=True
    )
    logger.info(f"✨ নতুন মুভি সেভ হয়েছে: {file.file_name}")

# ৬. স্টার্ট কমান্ড
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(f"হ্যালো {message.from_user.first_name}!\nআমি অনলাইনে আছি। মুভির নাম লিখে সার্চ দিন।")

# ৭. সার্চিং লজিক
@app.on_message(filters.text & filters.private)
async def search_movie(client, message):
    query = message.text
    cursor = movies_col.find({"file_name": {"$regex": query, "$options": "i"}})
    results = await cursor.to_list(length=10)
    
    if results:
        for movie in results:
            await message.reply_document(document=movie["file_id"], caption=movie['file_name'])
    else:
        await message.reply_text("দুঃখিত, এই নামে কোনো মুভি খুঁজে পাওয়া যায়নি।")

# ৮. মেইন রানার
async def main():
    threading.Thread(target=run_health_check, daemon=True).start()
    await app.start()
    logger.info("✅ বট সফলভাবে চালু হয়েছে!")
    # সাময়িকভাবে এই লাইনটি কমেন্ট (#) করে দিন যাতে বট চালু হওয়ার সময় ব্লক না হয়
    # await auto_index_all_movies()
    # বট চালু হওয়ার সাথে সাথে পুরনো মুভি ইনডেক্স করবে
    await auto_index_all_movies()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
