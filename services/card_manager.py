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
        """Get next card in learning phase"""
        cards = await storage.get_user_cards(telegram_id)
        
        # Find first card in learning status that hasn't been reviewed
        for card in cards:
            if card.status == 'learning' and card.last_reviewed is None:
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
            learning_cards = [c for c in cards if c.status == 'learning']
            completed = sum(1 for c in learning_cards if c.last_reviewed is not None)
            return completed, len(learning_cards)
    
    async def get_cards_for_review(self, telegram_id: int) -> List[UserCard]:
        """Get cards that are due for review"""
        return await storage.get_due_cards(telegram_id)
    
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
        
        # If card is in learning phase and first time reviewed, move to review status
        if card.status == 'learning' and card.last_reviewed is None:
            card.status = 'review'
            card.interval_index = 0
            # Calculate next review based on response
            new_index, next_review = calculate_next_review(0, response_type)
            card.interval_index = new_index
            card.next_review_time = next_review.isoformat()
        else:
            # Card is in review phase
            new_index, next_review = calculate_next_review(card.interval_index, response_type)
            card.interval_index = new_index
            card.next_review_time = next_review.isoformat()
        
        card.last_reviewed = now.isoformat()
        
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
            
            # Note: session index will be updated when showing next card
            
            # Check if learning phase is completed
            if not user.learning_phase_completed:
                next_learning = await self.get_next_learning_card(telegram_id)
                if next_learning is None:
                    user.learning_phase_completed = True
            
            await storage.save_user(user)
    
    async def is_learning_phase_completed(self, telegram_id: int) -> bool:
        """Check if user has completed learning phase"""
        user = await storage.get_user(telegram_id)
        return user.learning_phase_completed if user else False


# Global card manager instance
card_manager = CardManager()

