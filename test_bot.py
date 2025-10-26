#!/usr/bin/env python3
"""Quick test script to check bot configuration"""

import asyncio
from config import BOT_TOKEN

async def test_bot():
    from aiogram import Bot
    
    print(f"Testing bot with token: {BOT_TOKEN[:20]}...")
    
    try:
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Bot connected successfully!")
        print(f"   Username: @{me.username}")
        print(f"   Name: {me.first_name}")
        print(f"   ID: {me.id}")
        await bot.session.close()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_bot())
    exit(0 if success else 1)

