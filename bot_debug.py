import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from handlers import start, review

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main bot entry point with debug logging"""
    logger.info("=" * 60)
    logger.info("Bot starting in DEBUG mode...")
    logger.info("=" * 60)
    
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(review.router)
    
    logger.info(f"Routers registered:")
    logger.info(f"  - Start router: {start.router}")
    logger.info(f"  - Review router: {review.router}")
    logger.info(f"Total observers: {len(dp.observers)}")
    
    logger.info("=" * 60)
    logger.info("Starting polling... Send /start to the bot!")
    logger.info("=" * 60)
    
    # Start polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

