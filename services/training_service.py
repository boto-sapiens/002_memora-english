from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DEFAULT_PHRASES
import math

class TrainingService:
    """Service for training mode pagination and formatting"""
    
    PHRASES_PER_PAGE = 8
    
    def get_total_pages(self) -> int:
        """Calculate total pages for all phrases"""
        return math.ceil(len(DEFAULT_PHRASES) / self.PHRASES_PER_PAGE)
    
    def get_page_phrases(self, page: int) -> List[dict]:
        """Get phrases for specific page (1-indexed)"""
        if page < 1:
            page = 1
        
        start_idx = (page - 1) * self.PHRASES_PER_PAGE
        end_idx = start_idx + self.PHRASES_PER_PAGE
        
        return DEFAULT_PHRASES[start_idx:end_idx]
    
    def format_list_text(self, page: int) -> str:
        """Format list message text with phrases"""
        total_pages = self.get_total_pages()
        phrases = self.get_page_phrases(page)
        
        text = f"📚 Тренировка (стр. {page}/{total_pages})\n\n"
        
        for i, phrase in enumerate(phrases, 1):
            # Use English text, truncated if too long
            english_text = phrase["text_en"]
            if len(english_text) > 50:
                english_text = english_text[:47] + "..."
            text += f"{i}. {english_text}\n"
        
        return text.strip()
    
    def create_list_keyboard(self, page: int) -> InlineKeyboardMarkup:
        """Create keyboard with phrase buttons and navigation"""
        phrases = self.get_page_phrases(page)
        total_pages = self.get_total_pages()
        
        keyboard_rows = []
        
        # Add phrase buttons (8 per page)
        for i, phrase in enumerate(phrases, 1):
            # Truncate button text if too long
            button_text = phrase["text_en"]
            if len(button_text) > 30:
                button_text = button_text[:27] + "..."
            
            callback_data = f"tr:item:id={phrase['id']}:p={page}"
            keyboard_rows.append([InlineKeyboardButton(
                text=f"{i}. {button_text}",
                callback_data=callback_data
            )])
        
        # Add navigation buttons
        nav_buttons = []
        
        # Previous button
        if page > 1:
            nav_buttons.append(InlineKeyboardButton(
                text="⬅ Назад",
                callback_data=f"tr:page:prev:p={page}"
            ))
        
        # Next button
        if page < total_pages:
            nav_buttons.append(InlineKeyboardButton(
                text="➡ Вперёд",
                callback_data=f"tr:page:next:p={page}"
            ))
        
        if nav_buttons:
            keyboard_rows.append(nav_buttons)
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    def get_card_by_id(self, card_id: int) -> Optional[dict]:
        """Get phrase dict by ID from DEFAULT_PHRASES"""
        for phrase in DEFAULT_PHRASES:
            if phrase["id"] == card_id:
                return phrase
        return None
    
    def get_card_position(self, card_id: int) -> int:
        """Get position of card in total list (1-indexed)"""
        for i, phrase in enumerate(DEFAULT_PHRASES, 1):
            if phrase["id"] == card_id:
                return i
        return 0

# Global training service instance
training_service = TrainingService()
