from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.progress_service import progress_service
from datetime import datetime
import pytz
from config import TIMEZONE


router = Router()


@router.message(Command("progress"))
async def cmd_progress(message: Message):
    """Handle /progress command"""
    telegram_id = message.from_user.id
    
    stats = await progress_service.get_progress_stats(telegram_id)
    
    if not stats:
        await message.answer(
            "❌ Вы еще не начали обучение.\n"
            "Отправьте /start чтобы начать!",
            parse_mode="HTML"
        )
        return
    
    # Format next review time
    if stats['next_review_time']:
        tz = pytz.timezone(TIMEZONE)
        next_time = stats['next_review_time'].astimezone(tz)
        next_time_str = next_time.strftime("%d.%m.%Y %H:%M")
    else:
        next_time_str = "все повторения завершены"
    
    # Build message
    text = (
        f"📊 <b>Ваш прогресс:</b>\n\n"
        f"📚 Всего словосочетаний: {stats['total_cards']}\n"
        f"✅ Изучено: {stats['learned_cards']}\n"
        f"⏰ Ожидают повторения: {stats['due_cards']}\n"
        f"📅 Следующее повторение: {next_time_str}\n\n"
        f"<b>Статистика ответов:</b>\n"
        f"✅ Знал: {stats['knew_count']} раз\n"
        f"🤔 Сомневался: {stats['doubt_count']} раз\n"
        f"❌ Не знал: {stats['forgot_count']} раз\n\n"
        f"🔥 Серия дней подряд: {stats['current_streak']}\n"
        f"📝 Всего повторений: {stats['total_reviews']}"
    )
    
    await message.answer(text, parse_mode="HTML")

