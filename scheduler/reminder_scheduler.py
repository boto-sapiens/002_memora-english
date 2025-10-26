import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from storage.json_storage import storage
from services.card_manager import card_manager
from services.anki_algorithm import get_current_time
from config import CHECK_INTERVAL, BOT_TOKEN
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReminderScheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def check_and_notify_users(self):
        """Check all users and send notifications for due cards"""
        try:
            users = await storage.get_all_users()
            logger.info(f"Checking {len(users)} users for due cards...")
            
            for user in users:
                # Skip users who haven't completed learning phase
                if not user.learning_phase_completed:
                    continue
                
                # Get cards due for review
                due_cards = await card_manager.get_cards_for_review(user.telegram_id)
                
                if due_cards:
                    # Check if we already sent a notification recently (within last hour)
                    if user.last_notification_time:
                        last_notif = datetime.fromisoformat(user.last_notification_time)
                        if get_current_time() - last_notif < timedelta(hours=1):
                            continue
                    
                    # Send notification
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="🔄 Начать повторение", callback_data="start_review")]
                    ])
                    
                    try:
                        await self.bot.send_message(
                            chat_id=user.telegram_id,
                            text=f"🔔 У вас есть <b>{len(due_cards)}</b> карточек для повторения!\n\n"
                                 f"Время повторить изученные словосочетания.",
                            reply_markup=keyboard,
                            parse_mode="HTML"
                        )
                        
                        # Update last notification time
                        user.last_notification_time = get_current_time().isoformat()
                        await storage.save_user(user)
                        
                        logger.info(f"Sent notification to user {user.telegram_id} ({len(due_cards)} cards)")
                    except Exception as e:
                        logger.error(f"Failed to send notification to {user.telegram_id}: {e}")
        
        except Exception as e:
            logger.error(f"Error in check_and_notify_users: {e}")
    
    async def run(self):
        """Run scheduler loop"""
        logger.info(f"Scheduler started. Checking every {CHECK_INTERVAL} seconds...")
        
        while True:
            try:
                await self.check_and_notify_users()
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
            
            await asyncio.sleep(CHECK_INTERVAL)


async def start_scheduler():
    """Initialize and start scheduler"""
    bot = Bot(token=BOT_TOKEN)
    scheduler = ReminderScheduler(bot)
    await scheduler.run()

