from typing import Optional, List
from datetime import datetime
from storage.json_storage import storage
from storage.models import User, UserCard
from services.anki_algorithm import calculate_next_review, get_current_time


class CardManager:
    async def start_learning_phase(self, telegram_id: int, username: Optional[str] = None):
        """Start learning phase for a new user"""
        # Create user
        user = User(
            telegram_id=telegram_id,
            username=username,
            created_at=get_current_time().isoformat(),
            learning_phase_completed=False
        )
        await storage.save_user(user)
        
        # Initialize all cards
        await storage.init_learning_cards(telegram_id)
        
        # Initialize learning session
        cards = await storage.get_user_cards(telegram_id)
        user.current_session_total = len(cards)  # Total cards (21), not just learning cards
        user.current_session_index = 0
        await storage.save_user(user)
    
    async def get_next_learning_card(self, telegram_id: int) -> Optional[UserCard]:
        """Get next card for learning - returns cards by card_id order (new or pending), excluding learned"""
        cards = await storage.get_user_cards(telegram_id)
        
        # Sort by card_id
        cards.sort(key=lambda c: c.card_id)
        
        # Find first new or pending card (not learned)
        for card in cards:
            if card.status in ['new', 'pending']:
                return card
        
        return None
    
    async def get_learning_progress(self, telegram_id: int) -> tuple[int, int]:
        """Get learning progress (completed, total)"""
        user = await storage.get_user(telegram_id)
        if user and user.current_session_total:
            # Use saved session values - return current index (0-based) and total
            completed = user.current_session_index
            total = user.current_session_total
            return completed, total
        else:
            # Fallback to dynamic calculation
            cards = await storage.get_user_cards(telegram_id)
            # Count cards by status
            not_learned = [c for c in cards if c.status != 'learned']
            return 0, len(not_learned)
    
    async def get_cards_for_review(self, telegram_id: int) -> List[UserCard]:
        """Get cards that are due for review - sorted by card_id"""
        cards = await storage.get_due_cards(telegram_id)
        # Sort by card_id for consistent order
        cards.sort(key=lambda c: c.card_id)
        return cards
    
    async def process_response(self, telegram_id: int, card_id: int, response_type: str):
        """
        Process user response to a card
        
        Args:
            telegram_id: User's telegram ID
            card_id: Card ID
            response_type: 'forgot', 'uncertain', or 'knew'
        """
        cards = await storage.get_user_cards(telegram_id)
        card = next((c for c in cards if c.card_id == card_id), None)
        
        if not card:
            return
        
        now = get_current_time()
        
        # Calculate next review using new ANKI algorithm
        new_index, next_review, new_status = calculate_next_review(
            card.interval_index, 
            response_type, 
            card.status
        )
        
        # Update card
        card.interval_index = new_index
        card.next_review_time = next_review.isoformat()
        card.status = new_status
        card.last_reviewed = now.isoformat()
        card.last_response_type = response_type
        
        # Save updated card
        await storage.save_user_card(card)
        
        # Update user statistics
        user = await storage.get_user(telegram_id)
        if user:
            user.total_reviews += 1
            
            if response_type == 'knew':
                user.knew_count += 1
            elif response_type == 'uncertain':
                user.doubt_count += 1
            elif response_type == 'forgot':
                user.forgot_count += 1
            
            # Update streak
            today = get_current_time().date().isoformat()
            if user.last_activity_date:
                last_date = datetime.fromisoformat(user.last_activity_date).date()
                current_date = get_current_time().date()
                days_diff = (current_date - last_date).days
                
                if days_diff == 0:
                    # Activity already today
                    pass
                elif days_diff == 1:
                    # Activity yesterday - continue streak
                    user.current_streak += 1
                else:
                    # Gap - reset streak
                    user.current_streak = 1
            else:
                # First activity
                user.current_streak = 1
            
            user.last_activity_date = today
            
            await storage.save_user(user)
    
    async def is_learning_phase_completed(self, telegram_id: int) -> bool:
        """Check if user has completed learning phase"""
        user = await storage.get_user(telegram_id)
        return user.learning_phase_completed if user else False


# Global card manager instance
card_manager = CardManager()

