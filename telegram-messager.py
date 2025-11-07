import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import random

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
TARGET = os.getenv("TARGET")
INTERVAL = int(os.getenv("INTERVAL", 180))
MESSAGES = os.getenv("MESSAGES").split("؛")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    print("Client started successfully ✅")
    await client.start()

    while True:
        try:
            msg = random.choice(MESSAGES)
            await client.send_message(int(TARGET), msg)
            print(f"✅ Message sent: {msg}")
        except Exception as e:
            print("⚠️ Error sending message:", e)
        await asyncio.sleep(INTERVAL)

with client:
    client.loop.run_until_complete(main())