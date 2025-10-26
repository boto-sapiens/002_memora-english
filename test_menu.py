#!/usr/bin/env python3
"""Test bot commands menu"""

import asyncio
from aiogram import Bot
from config import BOT_TOKEN


async def test_menu():
    """Check if bot commands are set"""
    bot = Bot(token=BOT_TOKEN)
    
    try:
        commands = await bot.get_my_commands()
        
        print("=" * 60)
        print("Bot Commands Menu")
        print("=" * 60)
        print()
        
        if commands:
            print(f"✅ {len(commands)} commands registered:\n")
            for cmd in commands:
                print(f"   /{cmd.command} - {cmd.description}")
        else:
            print("❌ No commands set")
        
        print()
        print("=" * 60)
        
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(test_menu())

