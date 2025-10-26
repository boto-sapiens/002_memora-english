#!/usr/bin/env python3
"""Check which cards are due now"""

import asyncio
from datetime import datetime
import pytz
from storage.json_storage import storage
from services.anki_algorithm import get_current_time


async def check():
    user_id = 7742103512
    cards = await storage.get_user_cards(user_id)
    
    now_moscow = get_current_time()
    now_system = datetime.now()
    
    print("=" * 70)
    print("CARDS DUE CHECK")
    print("=" * 70)
    
    print(f"\nСистемное время: {now_system} (UTC+7 Бангкок)")
    print(f"Московское время: {now_moscow} (UTC+3)")
    print(f"Разница: 4 часа")
    
    print(f"\n{'='*70}")
    print("АНАЛИЗ КАРТОЧЕК:")
    print(f"{'='*70}\n")
    
    due_now = []
    future = []
    
    for card in cards:
        next_review = datetime.fromisoformat(card.next_review_time)
        diff_seconds = (next_review - now_moscow).total_seconds()
        diff_hours = diff_seconds / 3600
        
        # Convert to Bangkok time for display
        bangkok_tz = pytz.timezone('Asia/Bangkok')
        next_review_bangkok = next_review.astimezone(bangkok_tz)
        
        if diff_seconds <= 0:
            due_now.append((card, diff_hours))
        else:
            future.append((card, diff_hours, next_review_bangkok))
    
    print(f"📊 Просроченные карточки (ready now): {len(due_now)}")
    if due_now:
        for card, diff in due_now[:5]:
            print(f"   Card {card.card_id}: просрочено на {abs(diff):.1f}ч")
    
    print(f"\n⏰ Будущие карточки: {len(future)}")
    if future:
        print(f"\n   Ближайшие 5:")
        for card, diff, bkk_time in sorted(future, key=lambda x: x[1])[:5]:
            print(f"   Card {card.card_id}:")
            print(f"     Через: {diff:.1f}ч (~{diff/24:.1f} дней)")
            print(f"     По МСК: {card.next_review_time}")
            print(f"     По вашему: {bkk_time.strftime('%d.%m.%Y %H:%M')}")
            print(f"     Interval index: {card.interval_index}")
            print()
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(check())

