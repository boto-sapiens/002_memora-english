from typing import Optional
from storage.json_storage import storage
from storage.models import User, UserCard, SessionState
from services.card_manager import card_manager
import logging

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages learning and review sessions"""
    
    async def get_session_state(self, telegram_id: int) -> Optional[SessionState]:
        """Get current session state for user"""
        user = await storage.get_user(telegram_id)
        if not user:
            return None
        
        # Get all cards that need review (new or pending)
        next_card = await card_manager.get_next_learning_card(telegram_id)
        
        # If no cards need review - session completed
        if not next_card:
            return SessionState(
                current_index=0,
                total_in_session=0,
                phase='review',
                is_completed=True
            )
        
        # Initialize session if not set
        if user.current_session_total is None:
            cards = await storage.get_user_cards(telegram_id)
            # Count cards that need review (not learned)
            cards_to_review = [c for c in cards if c.status != 'learned']
            user.current_session_total = len(cards_to_review)
            user.current_session_index = 0
            await storage.save_user(user)
        
        return SessionState(
            current_index=user.current_session_index,
            total_in_session=user.current_session_total,
            phase='learning',
            is_completed=False
        )
    
    async def increment_session_index(self, telegram_id: int) -> None:
        """Increment current session index"""
        user = await storage.get_user(telegram_id)
        if user:
            user.current_session_index += 1
            await storage.save_user(user)
            logger.info(f"Incremented session index for user {telegram_id} to {user.current_session_index}")
    
    async def reset_session(self, telegram_id: int) -> None:
        """Reset session counters"""
        user = await storage.get_user(telegram_id)
        if user:
            user.current_session_total = None
            user.current_session_index = 0
            await storage.save_user(user)
            logger.info(f"Reset session for user {telegram_id}")
    
    async def get_next_card(self, telegram_id: int) -> Optional[UserCard]:
        """Get next card for current session (new or pending, in order by card_id)"""
        session_state = await self.get_session_state(telegram_id)
        if not session_state or session_state.is_completed:
            return None
        
        # Always use the same logic - get next card by order
        return await card_manager.get_next_learning_card(telegram_id)
    
    async def initialize_learning_session(self, telegram_id: int) -> None:
        """Initialize learning session for new user"""
        user = await storage.get_user(telegram_id)
        if user:
            cards = await storage.get_user_cards(telegram_id)
            user.current_session_total = len(cards)
            user.current_session_index = 0
            await storage.save_user(user)
            logger.info(f"Initialized learning session for user {telegram_id} with {len(cards)} cards")
    
    async def is_session_completed(self, telegram_id: int) -> bool:
        """Check if current session is completed"""
        session_state = await self.get_session_state(telegram_id)
        return session_state.is_completed if session_state else True


# Global session manager instance
session_manager = SessionManager()
