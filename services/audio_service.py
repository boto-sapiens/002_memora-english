from pathlib import Path
from aiogram import Bot
from aiogram.types import FSInputFile, InputMediaAudio, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest
from storage.json_storage import storage
import logging

logger = logging.getLogger(__name__)


class AudioService:
    def __init__(self):
        self.audio_dir = Path("audio")
        self.teacher_dir = self.audio_dir / "teacher"
        self.actor_dir = self.audio_dir / "actor"
    
    async def get_teacher_media(self, card_id: int, user_id: int):
        """
        Get teacher audio media for inline playback
        
        Returns InputMediaAudio if audio is available, None otherwise
        """
        cards = await storage.get_user_cards(user_id)
        card = next((c for c in cards if c.card_id == card_id), None)
        
        if not card:
            logger.warning(f"Card {card_id} not found for user {user_id}")
            return None
        
        # Try to use cached file_id first
        if card.file_id_teacher:
            try:
                return InputMediaAudio(media=card.file_id_teacher)
            except Exception as e:
                logger.warning(f"Cached file_id invalid for card {card_id}: {e}")
                # file_id expired or invalid, will try to load from file
        
        # Try to load audio file
        if card.audio_teacher:
            audio_path = self.teacher_dir / card.audio_teacher
            
            if audio_path.exists():
                try:
                    audio_file = FSInputFile(audio_path)
                    return InputMediaAudio(media=audio_file)
                except Exception as e:
                    logger.error(f"Error loading teacher audio for card {card_id}: {e}")
                    return None
            else:
                logger.warning(f"Teacher audio file not found: {audio_path}")
                return None
        
        logger.warning(f"No teacher audio configured for card {card_id}")
        return None
    
    async def get_actor_media(self, card_id: int, user_id: int):
        """
        Get actor audio media for inline playback
        
        Returns InputMediaAudio if audio is available, None otherwise
        """
        cards = await storage.get_user_cards(user_id)
        card = next((c for c in cards if c.card_id == card_id), None)
        
        if not card:
            logger.warning(f"Card {card_id} not found for user {user_id}")
            return None
        
        # Try to use cached file_id first
        if card.file_id_actor:
            try:
                return InputMediaAudio(media=card.file_id_actor)
            except Exception as e:
                logger.warning(f"Cached file_id invalid for card {card_id}: {e}")
                # file_id expired or invalid, will try to load from file
        
        # Try to load audio file
        if card.audio_actor:
            audio_path = self.actor_dir / card.audio_actor
            
            if audio_path.exists():
                try:
                    audio_file = FSInputFile(audio_path)
                    return InputMediaAudio(media=audio_file)
                except Exception as e:
                    logger.error(f"Error loading actor audio for card {card_id}: {e}")
                    return None
            else:
                logger.warning(f"Actor audio file not found: {audio_path}")
                return None
        
        logger.warning(f"No actor audio configured for card {card_id}")
        return None
    
    async def cache_file_id(self, card_id: int, user_id: int, file_id: str, audio_type: str):
        """
        Cache file_id for future use
        
        Args:
            card_id: Card ID
            user_id: User ID
            file_id: Telegram file_id
            audio_type: 'teacher' or 'actor'
        """
        cards = await storage.get_user_cards(user_id)
        card = next((c for c in cards if c.card_id == card_id), None)
        
        if not card:
            logger.warning(f"Card {card_id} not found for user {user_id}")
            return
        
        if audio_type == 'teacher':
            card.file_id_teacher = file_id
        elif audio_type == 'actor':
            card.file_id_actor = file_id
        
        await storage.save_user_card(card)
        logger.info(f"Cached {audio_type} file_id for card {card_id}")


# Global audio service instance
audio_service = AudioService()