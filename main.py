import os, asyncio, logging, http.server, socketserver, threading
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ১. সেটিংস
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DATABASE_URI = os.environ.get("DATABASE_URI", "")
CHANNEL_ID = int(os.environ.get("CHANNELS", "0"))
ADMINS = [int(id) for id in os.environ.get("ADMINS", "").split()]

# ২. ডাটাবেস
db_client = AsyncIOMotorClient(DATABASE_URI)
db = db_client["movie_bot"]
movies_col = db["movies"]

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ৩. হেলথ চেক
def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# --- নতুন ফিচার: সব পুরনো মুভি ইনডেক্স করার কমান্ড ---
@app.on_message(filters.command("index") & filters.user(ADMINS))
async def manual_index(client, message):
    msg = await message.reply_text("চ্যানেলের মুভিগুলো ইনডেক্স করা শুরু হচ্ছে... একটু অপেক্ষা করুন।")
    count = 0
    async for user_msg in client.get_chat_history(CHANNEL_ID):
        if user_msg.document or user_msg.video:
            file = user_msg.document or user_msg.video
            file_name = file.file_name
            file_id = file.file_id
            
            await movies_col.update_one(
                {"file_name": file_name},
                {"$set": {"file_id": file_id, "caption": user_msg.caption or file_name}},
                upsert=True
            )
            count += 1
    await msg.edit(f"✅ সফলভাবে {count}টি মুভি ইনডেক্স করা হয়েছে!")

# সার্চিং ফিচার
@app.on_message(filters.text & filters.private)
async def search_movie(client, message):
    query = message.text
    cursor = movies_col.find({"file_name": {"$regex": query, "$options": "i"}})
    results = await cursor.to_list(length=10)
    
    if results:
        for movie in results:
            await message.reply_document(document=movie["file_id"], caption=movie['file_name'])
    else:
        await message.reply_text("দুঃখিত, এই নামে কোনো মুভি পাওয়া যায়নি।")

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    app.run()
