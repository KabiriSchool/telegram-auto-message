# telegram-messager.py
import os, asyncio, random, logging
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from aiohttp import web

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# -----------------------
# Load environment variables
# -----------------------
API_ID = int(os.getenv("API_ID", "2040"))
API_HASH = os.getenv("API_HASH", "b18441a1ff607e10a989891a5462e627")
SESSION_STRING = os.getenv("SESSION_STRING", "")
TARGET1 = os.getenv("TARGET1", "")
TARGET2 = os.getenv("TARGET2", "")
INTERVAL = int(os.getenv("INTERVAL", "180"))
MESSAGES = os.getenv("MESSAGES", "سلام").split("؛")
JITTER = int(os.getenv("JITTER", "0"))
PORT = int(os.getenv("PORT", "3000"))

# -----------------------
# Debug print to verify .env
# -----------------------
print("===== DEBUG: .env values =====")
print("API_ID:", repr(API_ID))
print("API_HASH:", repr(API_HASH[:10] + "..."))
print("SESSION_STRING:", "Loaded" if SESSION_STRING else "EMPTY ❌")
print("TARGET1:", repr(TARGET1))
print("TARGET2:", repr(TARGET2))
print("INTERVAL:", INTERVAL)
print("MESSAGES:", MESSAGES)
print("JITTER:", JITTER)
print("PORT:", PORT)
print("==============================")

# -----------------------
# Initialize Telegram client
# -----------------------
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH, connection_retries=5)

async def send_loop():
    await client.start()
    logging.info("Telegram client started.")

    while True:
        start_time = asyncio.get_event_loop().time()
        try:
            msg = random.choice(MESSAGES).strip() or "سلام"

            # ارسال به گروه اول (در صورت وجود)
            if TARGET1.strip():
                logging.info(f"Sending to {TARGET1}: {msg}")
                await client.send_message(int(TARGET1), msg)
                await asyncio.sleep(2)
            else:
                logging.warning("TARGET1 is empty, skipping.")

            # ارسال به گروه دوم (در صورت وجود)
            if TARGET2.strip():
                logging.info(f"Sending to {TARGET2}: {msg}")
                await client.send_message(int(TARGET2), msg)
            else:
                logging.warning("TARGET2 is empty, skipping.")

            elapsed = asyncio.get_event_loop().time() - start_time
            wait = max(0, INTERVAL - elapsed)
            logging.info(f"Next message in {wait:.1f}s")
            await asyncio.sleep(wait)

        except errors.FloodWaitError as e:
            logging.warning(f"FloodWait {e.seconds}s — sleeping")
            await asyncio.sleep(e.seconds + 5)
        except Exception:
            logging.exception("Error sending — retrying after short delay")
            await asyncio.sleep(30)

async def keep_alive():
    app = web.Application()
    async def handle(req): return web.Response(text="ok")
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logging.info(f"Keep-alive server on port {PORT}")

async def main():
    await keep_alive()
    await send_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stopped")
