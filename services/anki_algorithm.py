from datetime import datetime, timedelta
import pytz
from config import INTERVALS, TIMEZONE


def get_current_time():
    """Get current time in configured timezone"""
    tz = pytz.timezone(TIMEZONE)
    return datetime.now(tz)


def calculate_next_review(current_index: int, response_type: str, current_status: str = "new") -> tuple[int, datetime, str]:
    """
    Calculate next review time and new status based on ANKI algorithm
    
    Args:
        current_index: Current interval index (0-10)
        response_type: 'forgot', 'uncertain', or 'knew'
        current_status: Current card status ('new', 'learning', 'pending', 'learned')
    
    Returns:
        Tuple of (new_interval_index, next_review_datetime, new_status)
    """
    now = get_current_time()
    MAX_INDEX = len(INTERVALS) - 1  # 10
    
    if response_type == 'forgot':
        # ❌ Не знал → сброс на начальный интервал, статус learning
        new_index = 0
        new_status = 'learning'
    elif response_type == 'uncertain':
        # 🤔 Сомневался → оставить текущий интервал, статус learning
        new_index = current_index
        new_status = 'learning'
    elif response_type == 'knew':
        # ✅ Знал легко → увеличить интервал
        new_index = min(current_index + 1, MAX_INDEX)
        # Если достигли максимального интервала - статус learned
        if new_index >= MAX_INDEX:
            new_status = 'learned'
        else:
            new_status = 'learning'
    else:
        raise ValueError(f"Unknown response type: {response_type}")
    
    # Calculate next review time
    interval_seconds = INTERVALS[new_index]
    next_review = now + timedelta(seconds=interval_seconds)
    
    return new_index, next_review, new_status


def format_interval(index: int) -> str:
    """Format interval for display"""
    intervals_display = [
        "1 час", "4 часа", "1 день", "3 дня", "7 дней",
        "14 дней", "30 дней", "60 дней", "90 дней", "180 дней", "365 дней"
    ]
    return intervals_display[index] if 0 <= index < len(intervals_display) else "неизвестно"

