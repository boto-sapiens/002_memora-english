from datetime import datetime, timedelta
import pytz
from config import INTERVALS, TIMEZONE


def get_current_time():
    """Get current time in configured timezone"""
    tz = pytz.timezone(TIMEZONE)
    return datetime.now(tz)


def calculate_next_review(current_index: int, response_type: str) -> tuple[int, datetime]:
    """
    Calculate next review time based on ANKI algorithm
    
    Args:
        current_index: Current interval index (0-10)
        response_type: 'forgot', 'uncertain', or 'knew'
    
    Returns:
        Tuple of (new_interval_index, next_review_datetime)
    """
    now = get_current_time()
    
    if response_type == 'forgot':
        # ❌ Не знал → сброс на начальный интервал
        new_index = 0
    elif response_type == 'uncertain':
        # 🤔 Сомневался → оставить текущий интервал
        new_index = current_index
    elif response_type == 'knew':
        # ✅ Знал легко → увеличить интервал
        new_index = min(current_index + 1, len(INTERVALS) - 1)
    else:
        raise ValueError(f"Unknown response type: {response_type}")
    
    # Calculate next review time
    interval_seconds = INTERVALS[new_index]
    next_review = now + timedelta(seconds=interval_seconds)
    
    return new_index, next_review


def format_interval(index: int) -> str:
    """Format interval for display"""
    intervals_display = [
        "1 час", "4 часа", "1 день", "3 дня", "7 дней",
        "14 дней", "30 дней", "60 дней", "90 дней", "180 дней", "365 дней"
    ]
    return intervals_display[index] if 0 <= index < len(intervals_display) else "неизвестно"

