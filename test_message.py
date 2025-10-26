#!/usr/bin/env python3
"""Test sending a message to verify bot can send"""

import asyncio
from aiogram import Bot
from config import BOT_TOKEN

async def test_send():
    bot = Bot(token=BOT_TOKEN)
    
    # Your telegram ID from users.json
    user_id = 7742103512
    
    try:
        await bot.send_message(
            chat_id=user_id,
            text="🧪 **Test message**\n\nIf you see this, bot can send messages!"
        )
        print("✅ Test message sent successfully!")
    except Exception as e:
        print(f"❌ Error sending message: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_send())

