import os, asyncio, random, logging
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from aiohttp import web

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

API_ID = int(os.getenv("API_ID", "2040"))
API_HASH = os.getenv("API_HASH", "b18441a1ff607e10a989891a5462e627")
SESSION_STRING = os.getenv("SESSION_STRING", "")
TARGET1 = os.getenv("TARGET1", "")
TARGET2 = os.getenv("TARGET2", "")
MESSAGES = os.getenv("MESSAGES").split("؛")
PORT = int(os.getenv("PORT", "5000"))

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


async def send_loop():
    await client.start()
    logging.info("Telegram client started.")

    while True:
        msg = random.choice(MESSAGES).strip() or "یا حسین"
        try:
            # ارسال به گروه اول
            if TARGET1:
                logging.info(f"Sending to {TARGET1}: {msg}")
                await client.send_message(int(TARGET1), msg)
                await asyncio.sleep(random.uniform(2, 6)
                                    )  # تأخیر تصادفی بین ارسال‌ها

            # ارسال به گروه دوم
            if TARGET2:
                logging.info(f"Sending to {TARGET2}: {msg}")
                await client.send_message(int(TARGET2), msg)

            # فاصله تصادفی بین 4 تا 7 دقیقه
            interval = random.randint(240, 420)
            logging.info(
                f"Next message in {interval} seconds (~{interval//60} min)")
            await asyncio.sleep(interval)

        except errors.FloodWaitError as e:
            logging.warning(f"FloodWait {e.seconds}s — sleeping")
            await asyncio.sleep(e.seconds + 5)
        except Exception:
            logging.exception("Error sending — retrying after short delay")
            await asyncio.sleep(30)


async def keep_alive():
    app = web.Application()

    async def handle(req):
        return web.Response(text="ok")

    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logging.info(f"Keep-alive server running on port {PORT}")


async def main():
    await keep_alive()
    await send_loop()


if __name__ == "__main__":
    asyncio.run(main())
