#!/usr/bin/env python3
"""Test that handlers are registered correctly"""

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from handlers import start, review

async def test_handlers():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(review.router)
    
    print("✅ Bot initialized")
    print(f"   Start router: {start.router}")
    print(f"   Review router: {review.router}")
    print(f"   Registered handlers: {len(dp.observers)}")
    
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_handlers())

