from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from storage.json_storage import storage
from services.anki_algorithm import get_current_time
from datetime import datetime
import pytz
from config import TIMEZONE


router = Router()


def format_time_remaining(time_str: str, now: datetime) -> str:
    """Format remaining time as 'Xч Yм'"""
    if not time_str:
        return ""
    
    target_time = datetime.fromisoformat(time_str)
    diff_seconds = (target_time - now).total_seconds()
    
    if diff_seconds <= 0:
        return "истекло"
    
    hours = int(diff_seconds // 3600)
    minutes = int((diff_seconds % 3600) // 60)
    
    if hours > 0:
        return f"{hours}ч {minutes:02d}м"
    else:
        return f"{minutes}м"


def get_status_icon(status: str) -> str:
    """Get icon for card status"""
    icons = {
        'new': '🎯',
        'learning': '🔁',
        'pending': '⏳',
        'learned': '✅'
    }
    return icons.get(status, '❓')


@router.message(Command("progress"))
async def cmd_progress(message: Message):
    """Handle /progress command - show all cards with their statuses"""
    telegram_id = message.from_user.id
    
    # Get user and cards
    user = await storage.get_user(telegram_id)
    if not user:
        await message.answer(
            "❌ Вы еще не начали обучение.\n"
            "Отправьте /start чтобы начать!",
            parse_mode="HTML"
        )
        return
    
    cards = await storage.get_user_cards(telegram_id)
    if not cards:
        await message.answer(
            "❌ У вас нет карточек.\n"
            "Отправьте /start чтобы начать!",
            parse_mode="HTML"
        )
        return
    
    # Sort by card_id
    cards.sort(key=lambda c: c.card_id)
    
    # Current time for calculations
    now = get_current_time()
    
    # Build card list
    card_lines = []
    for card in cards:
        icon = get_status_icon(card.status)
        status_name = card.status.upper()
        
        # Add time information
        time_info = ""
        if card.status == 'pending' and card.deadline_time:
            time_remaining = format_time_remaining(card.deadline_time, now)
            time_info = f" (осталось {time_remaining})"
        elif card.status == 'learning' and card.next_review_time:
            time_remaining = format_time_remaining(card.next_review_time, now)
            time_info = f" (повтор через {time_remaining})"
        
        card_lines.append(f"{card.card_id}. {icon} {status_name}{time_info}")
    
    # Build summary statistics
    new_count = sum(1 for c in cards if c.status == 'new')
    learning_count = sum(1 for c in cards if c.status == 'learning')
    pending_count = sum(1 for c in cards if c.status == 'pending')
    learned_count = sum(1 for c in cards if c.status == 'learned')
    
    # Build final message
    text = "📊 <b>Прогресс изучения</b>\n\n"
    text += "\n".join(card_lines)
    text += f"\n\n<b>Итого:</b>\n"
    text += f"🎯 Новые: {new_count}\n"
    text += f"🔁 Изучаемые: {learning_count}\n"
    text += f"⏳ Ожидают: {pending_count}\n"
    text += f"✅ Изучено: {learned_count}\n"
    text += f"\n🔥 Серия: {user.current_streak} дней"
    
    await message.answer(text, parse_mode="HTML")

