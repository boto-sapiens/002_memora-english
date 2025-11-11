import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import start, review, progress, help, group_stats, training, group_dictation, arena_control

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot):
    """Set bot commands menu"""
    commands = [
        BotCommand(command="start", description="🎓 Начать обучение"),
        BotCommand(command="training", description="📚 Режим тренировки"),
        BotCommand(command="progress", description="📊 Показать прогресс"),
        BotCommand(command="group_stats", description="👥 Статистика группы"),
        BotCommand(command="arena_status", description="🏟️ Arena статус"),
        BotCommand(command="help", description="❓ Помощь и список команд"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Main bot entry point"""
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Set commands menu
    await set_bot_commands(bot)
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(review.router)
    # dp.include_router(audio.router)  # Removed - using embedded audio now
    dp.include_router(training.router)
    dp.include_router(progress.router)
    dp.include_router(group_stats.router)
    dp.include_router(group_dictation.router)
    dp.include_router(arena_control.router)
    dp.include_router(help.router)
    
    logger.info("Bot starting...")
    
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

