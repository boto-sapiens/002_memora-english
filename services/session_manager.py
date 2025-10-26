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
        
        # Check if learning phase is completed
        is_learning_completed = await card_manager.is_learning_phase_completed(telegram_id)
        
        if not is_learning_completed:
            # Learning phase - используем сохраненные значения или инициализируем
            if user.current_session_total is None:
                cards = await storage.get_user_cards(telegram_id)
                user.current_session_total = len(cards)
                user.current_session_index = 0
                await storage.save_user(user)
            
            return SessionState(
                current_index=user.current_session_index,
                total_in_session=user.current_session_total,
                phase='learning',
                is_completed=False
            )
        else:
            # Review phase
            due_cards = await card_manager.get_cards_for_review(telegram_id)
            
            if not due_cards:
                return SessionState(
                    current_index=0,
                    total_in_session=0,
                    phase='review',
                    is_completed=True
                )
            
            # Инициализировать сессию review если не установлена
            if user.current_session_total is None or user.current_session_total == 0:
                user.current_session_total = len(due_cards)
                user.current_session_index = 0
                await storage.save_user(user)
            
            return SessionState(
                current_index=user.current_session_index,
                total_in_session=user.current_session_total,
                phase='review',
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
        """Get next card for current session"""
        session_state = await self.get_session_state(telegram_id)
        if not session_state or session_state.is_completed:
            return None
        
        if session_state.phase == 'learning':
            return await card_manager.get_next_learning_card(telegram_id)
        else:
            # Review phase
            due_cards = await card_manager.get_cards_for_review(telegram_id)
            return due_cards[0] if due_cards else None
    
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
