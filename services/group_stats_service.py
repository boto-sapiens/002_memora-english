from typing import List, Dict
from datetime import datetime
from storage.json_storage import storage
from services.anki_algorithm import get_current_time


class GroupStatsService:
    async def get_group_stats(self) -> Dict:
        """Get statistics for all users"""
        users = await storage.get_all_users()
        
        if not users:
            return None
        
        now = get_current_time()
        user_stats = []
        
        for user in users:
            cards = await storage.get_user_cards(user.telegram_id)
            
            # Calculate statistics for this user
            total_cards = len(cards)
            learned_cards = sum(1 for c in cards if c.status == 'review')
            due_cards = sum(1 for c in cards 
                           if c.status == 'review' 
                           and datetime.fromisoformat(c.next_review_time) <= now)
            
            # Display name (username or first name)
            display_name = f"@{user.username}" if user.username else f"User_{user.telegram_id}"
            
            user_stats.append({
                'display_name': display_name,
                'learned': learned_cards,
                'total': total_cards,
                'due': due_cards,
                'streak': user.current_streak,
                'total_reviews': user.total_reviews,
            })
        
        # Sort by progress (learned cards, descending)
        user_stats.sort(key=lambda x: x['learned'], reverse=True)
        
        # Limit to top 20
        user_stats = user_stats[:20]
        
        # Calculate average progress
        if user_stats:
            avg_progress = sum(u['learned'] / u['total'] * 100 if u['total'] > 0 else 0 
                             for u in user_stats) / len(user_stats)
        else:
            avg_progress = 0
        
        return {
            'users': user_stats,
            'total_users': len(users),
            'avg_progress': avg_progress,
        }


# Global group stats service instance
group_stats_service = GroupStatsService()

