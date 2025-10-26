#!/usr/bin/env python3
"""Debug time and timezone issues"""

import asyncio
from datetime import datetime
import pytz
from config import TIMEZONE
from services.anki_algorithm import get_current_time
from storage.json_storage import storage


async def debug_time():
    print("=" * 70)
    print("TIME DEBUG")
    print("=" * 70)
    
    # System time
    system_time = datetime.now()
    print(f"\n1. System time (naive): {system_time}")
    print(f"   ISO: {system_time.isoformat()}")
    
    # Configured timezone
    print(f"\n2. Configured TIMEZONE: {TIMEZONE}")
    
    # Current time in configured timezone
    current_time = get_current_time()
    print(f"\n3. Current time in {TIMEZONE}:")
    print(f"   {current_time}")
    print(f"   ISO: {current_time.isoformat()}")
    
    # Check user's cards
    user_id = 7742103512
    cards = await storage.get_user_cards(user_id)
    
    if cards:
        print(f"\n4. Sample card times (first 3):")
        for i, card in enumerate(cards[:3], 1):
            next_review = datetime.fromisoformat(card.next_review_time)
            diff = (next_review - current_time).total_seconds()
            status = "PAST (due)" if diff < 0 else f"FUTURE (in {diff/3600:.1f} hours)"
            
            print(f"\n   Card {card.card_id}:")
            print(f"     Text: {card.text[:40]}...")
            print(f"     Next review: {card.next_review_time}")
            print(f"     Status: {status}")
            print(f"     Interval index: {card.interval_index}")
    
    # Check due cards logic
    now = get_current_time()
    due_cards = [c for c in cards 
                 if c.status == 'review' 
                 and datetime.fromisoformat(c.next_review_time) <= now]
    
    print(f"\n5. Due cards count: {len(due_cards)}")
    if due_cards:
        print(f"   Cards ready for review:")
        for card in due_cards[:5]:
            print(f"     - Card {card.card_id}: {card.text[:40]}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(debug_time())

