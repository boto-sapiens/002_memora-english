import asyncio
import random
import logging
import json
import os
from datetime import datetime
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, TARGET_CHAT_ID, DEFAULT_PHRASES, ARENA_URL, ARENA_ENABLED
from services.arena_client import ArenaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Control file path
CONTROL_FILE = "data/arena_control.json"


def is_dictation_enabled():
    """Check if arena dictation is enabled."""
    if os.path.exists(CONTROL_FILE):
        try:
            with open(CONTROL_FILE, 'r') as f:
                data = json.load(f)
                return data.get('dictation_enabled', True)
        except Exception as e:
            logger.error(f"Error reading control file: {e}")
    return True  # Default: enabled


class GroupDictationScheduler:
    """Scheduler that sends random phrase cards to group chat every minute"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.phrases = DEFAULT_PHRASES
        self.arena_client = ArenaClient(ARENA_URL) if ARENA_ENABLED else None
        
    async def send_random_card(self):
        """Send a random phrase card via Arena Relay Bot or directly to TARGET_CHAT_ID"""
        # Check if dictation is enabled
        if not is_dictation_enabled():
            logger.debug("Arena dictation is disabled - skipping")
            return
        
        if TARGET_CHAT_ID is None and not ARENA_ENABLED:
            logger.warning("Neither TARGET_CHAT_ID nor ARENA is configured - skipping")
            return
        
        try:
            # Pick random phrase
            phrase = random.choice(self.phrases)
            
            # Send only English text (plain text for chronicler bot to process)
            text = phrase['text_en']
            
            # Send via Arena if enabled, otherwise send directly
            if self.arena_client and ARENA_ENABLED:
                success = await self.arena_client.say(text)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if success:
                    logger.info(f"[{timestamp}] Sent phrase {phrase['id']} via Arena: {text}")
                else:
                    logger.error(f"[{timestamp}] Failed to send phrase {phrase['id']} via Arena")
            else:
                # Fallback to direct sending
                await self.bot.send_message(
                    chat_id=TARGET_CHAT_ID,
                    text=text
                )
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"[{timestamp}] Sent phrase {phrase['id']} directly to chat {TARGET_CHAT_ID}: {text}")
            
        except Exception as e:
            logger.error(f"Error sending group dictation card: {e}")
    
    async def run(self, interval_seconds: int = 60):
        """Run scheduler loop - send card every interval_seconds"""
        if ARENA_ENABLED:
            logger.info(f"Group dictation scheduler started. Sending cards every {interval_seconds} seconds via Arena ({ARENA_URL})")
            # Check arena health on startup
            if self.arena_client:
                await self.arena_client.check_health()
        else:
            logger.info(f"Group dictation scheduler started. Sending cards every {interval_seconds} seconds to chat {TARGET_CHAT_ID}")
        
        while True:
            try:
                await self.send_random_card()
            except Exception as e:
                logger.error(f"Error in group dictation loop: {e}")
            
            await asyncio.sleep(interval_seconds)


async def start_group_dictation():
    """Initialize and start group dictation scheduler"""
    bot = Bot(token=BOT_TOKEN)
    scheduler = GroupDictationScheduler(bot)
    await scheduler.run(interval_seconds=60)  # Every 1 minute


if __name__ == "__main__":
    try:
        logger.info("Starting group dictation scheduler...")
        asyncio.run(start_group_dictation())
    except KeyboardInterrupt:
        logger.info("Group dictation scheduler stopped by user")

