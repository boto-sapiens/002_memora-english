#!/usr/bin/env python3
"""
Migrate existing users to add new statistics fields
"""

import asyncio
from storage.json_storage import storage


async def migrate():
    """Migrate all existing users to new schema"""
    users = await storage.get_all_users()
    
    print(f"Found {len(users)} users to migrate...")
    
    migrated = 0
    for user in users:
        # Always set the new fields (even if they exist but are None)
        if not hasattr(user, 'knew_count') or user.knew_count is None:
            user.knew_count = 0
        if not hasattr(user, 'doubt_count') or user.doubt_count is None:
            user.doubt_count = 0
        if not hasattr(user, 'forgot_count') or user.forgot_count is None:
            user.forgot_count = 0
        if not hasattr(user, 'current_streak') or user.current_streak is None:
            user.current_streak = 0
        if not hasattr(user, 'total_reviews') or user.total_reviews is None:
            user.total_reviews = 0
        if not hasattr(user, 'last_activity_date'):
            user.last_activity_date = None
        
        await storage.save_user(user)
        migrated += 1
        print(f"  Migrated user {user.telegram_id} (@{user.username})")
    
    print(f"\n✅ Migration complete!")
    print(f"   Total users: {len(users)}")
    print(f"   Migrated: {migrated}")
    print(f"   Already up-to-date: {len(users) - migrated}")


if __name__ == "__main__":
    print("=" * 60)
    print("FilevskiyBot User Migration")
    print("=" * 60)
    print("\nAdding statistics fields to existing users...")
    print()
    
    asyncio.run(migrate())
    
    print("\n" + "=" * 60)
    print("Migration finished successfully!")
    print("=" * 60)

