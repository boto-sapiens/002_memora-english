from typing import Dict, Optional
from datetime import datetime
from storage.json_storage import storage
from services.anki_algorithm import get_current_time


class ProgressService:
    async def get_progress_stats(self, telegram_id: int) -> Optional[Dict]:
        """Get user progress statistics"""
        user = await storage.get_user(telegram_id)
        cards = await storage.get_user_cards(telegram_id)
        
        if not user:
            return None
        
        now = get_current_time()
        
        # Calculate statistics
        total_cards = len(cards)
        learned_cards = sum(1 for c in cards if c.status == 'review')
        due_cards = sum(1 for c in cards 
                       if c.status == 'review' 
                       and datetime.fromisoformat(c.next_review_time) <= now)
        
        # Next review time
        future_cards = [c for c in cards 
                       if c.status == 'review' 
                       and datetime.fromisoformat(c.next_review_time) > now]
        
        next_review = None
        if future_cards:
            next_review = min(datetime.fromisoformat(c.next_review_time) 
                            for c in future_cards)
        
        return {
            'total_cards': total_cards,
            'learned_cards': learned_cards,
            'due_cards': due_cards,
            'next_review_time': next_review,
            'knew_count': user.knew_count,
            'doubt_count': user.doubt_count,
            'forgot_count': user.forgot_count,
            'current_streak': user.current_streak,
            'total_reviews': user.total_reviews,
        }


# Global progress service instance
progress_service = ProgressService()

