#!/usr/bin/env python3
"""Test /progress command functionality"""

import asyncio
from services.progress_service import progress_service


async def test_progress():
    """Test progress statistics"""
    # Test with existing user
    user_id = 7742103512
    
    print("=" * 60)
    print("Testing /progress command")
    print("=" * 60)
    print()
    
    stats = await progress_service.get_progress_stats(user_id)
    
    if stats:
        print(f"✅ Statistics loaded for user {user_id}")
        print()
        print(f"📊 Progress:")
        print(f"   Total cards: {stats['total_cards']}")
        print(f"   Learned cards: {stats['learned_cards']}")
        print(f"   Due cards: {stats['due_cards']}")
        print(f"   Next review: {stats['next_review_time']}")
        print()
        print(f"📈 Statistics:")
        print(f"   Knew: {stats['knew_count']}")
        print(f"   Doubt: {stats['doubt_count']}")
        print(f"   Forgot: {stats['forgot_count']}")
        print(f"   Streak: {stats['current_streak']} days")
        print(f"   Total reviews: {stats['total_reviews']}")
    else:
        print(f"❌ No statistics found for user {user_id}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_progress())

