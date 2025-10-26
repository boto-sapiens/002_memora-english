#!/usr/bin/env python3
"""Test group stats functionality"""

import asyncio
from services.group_stats_service import group_stats_service


async def test():
    """Test group statistics"""
    print("=" * 70)
    print("Testing /group_stats command")
    print("=" * 70)
    print()
    
    stats = await group_stats_service.get_group_stats()
    
    if stats and stats['users']:
        print(f"✅ Group statistics loaded")
        print(f"\nTotal users: {stats['total_users']}")
        print(f"Average progress: {stats['avg_progress']:.1f}%")
        print(f"\nUsers in ranking:")
        
        for i, user in enumerate(stats['users'], 1):
            print(f"\n{i}. {user['display_name']}")
            print(f"   Learned: {user['learned']}/{user['total']}")
            print(f"   Due: {user['due']}")
            print(f"   Streak: {user['streak']} days")
            print(f"   Total reviews: {user['total_reviews']}")
    else:
        print("❌ No users found")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test())

