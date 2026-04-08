import os
import asyncio
import logging
import http.server
import socketserver
import threading
from pyrogram import Client, filters

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ১. হেলথ চেক সার্ভার (Render-এর 'No open ports' এরর বন্ধ করতে)
def run_health_check():
    # Render অটোমেটিক একটি PORT এনভায়রনমেন্ট ভেরিয়েবল দেয়
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logger.info(f"Health check server started on port {port}")
        httpd.serve_forever()

# ২. টেলিগ্রাম বট সেটআপ
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(f"হ্যালো {message.from_user.first_name}! আমি অনলাইনে আছি।")

async def run_bot():
    async with app:
        logger.info("✅ বট সফলভাবে চালু হয়েছে এবং মেসেজের জন্য প্রস্তুত!")
        await asyncio.Event().wait()

# ৩. মেইন ফাংশন
if __name__ == "__main__":
    # হেলথ চেক আলাদা থ্রেডে চালানো যেন Render পোর্ট খুঁজে পায়
    threading.Thread(target=run_health_check, daemon=True).start()

    # বট সরাসরি রান করা (এটিই মেসেজ হ্যান্ডেল করবে)
    print("✅ বট সফলভাবে চালু হয়েছে এবং মেসেজের জন্য প্রস্তুত!")
    app.run()
