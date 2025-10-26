#!/usr/bin/env python3
"""Check user status and next card"""

import asyncio
from storage.json_storage import storage
from services.card_manager import card_manager

async def check_status():
    user_id = 7742103512
    
    print(f"=== Checking user {user_id} ===\n")
    
    # Get user
    user = await storage.get_user(user_id)
    if user:
        print(f"✅ User exists")
        print(f"   Username: {user.username}")
        print(f"   Learning completed: {user.learning_phase_completed}")
    else:
        print("❌ User not found")
        return
    
    # Get next card
    next_card = await card_manager.get_next_learning_card(user_id)
    if next_card:
        print(f"\n✅ Next card found:")
        print(f"   ID: {next_card.card_id}")
        print(f"   Text: {next_card.text[:50]}...")
        print(f"   Status: {next_card.status}")
        print(f"   Last reviewed: {next_card.last_reviewed}")
    else:
        print("\n❌ No next card found")
    
    # Get progress
    completed, total = await card_manager.get_learning_progress(user_id)
    print(f"\n📊 Progress: {completed}/{total}")
    
    # Get all cards
    cards = await storage.get_user_cards(user_id)
    print(f"\n📚 Total cards: {len(cards)}")
    learning_cards = [c for c in cards if c.status == 'learning' and c.last_reviewed is None]
    print(f"   Learning (not reviewed): {len(learning_cards)}")

if __name__ == "__main__":
    asyncio.run(check_status())

