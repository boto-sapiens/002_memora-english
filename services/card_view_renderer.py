from typing import Union, Optional
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAudio
from storage.models import UserCard, SessionState
from services.audio_service import audio_service
import logging

logger = logging.getLogger(__name__)


class CardViewRenderer:
    """Renders card views in Telegram as single messages"""
    
    async def render_question(self, message_or_callback: Union[Message, CallbackQuery], 
                            card: UserCard, session_state: SessionState) -> None:
        """Render question phase: Russian text + 'Show answer' button"""
        russian_text = card.text_ru if card.text_ru else card.text
        progress_text = f"📊 Прогресс: {session_state.current_index + 1}/{session_state.total_in_session}"
        
        text = f"{progress_text}\n\n🇷🇺 <i>{russian_text}</i>"
        keyboard = self._get_show_answer_keyboard(card.card_id)
        
        await self._edit_message(message_or_callback, text, keyboard)
        logger.info(f"Rendered question for card {card.card_id}, user {card.user_id}")
    
    async def render_answer(self, message_or_callback: Union[Message, CallbackQuery], 
                          card: UserCard, session_state: SessionState, current_audio: str = "teacher") -> None:
        """Render answer phase: English text + transcription + ONE switchable audio player + evaluation buttons"""
        english_text = card.text_en if card.text_en else card.text
        transcription = card.transcription if card.transcription else ""
        progress_text = f"📊 Прогресс: {session_state.current_index + 1}/{session_state.total_in_session}"
        
        # Build text content
        text = f"{progress_text}\n\n🇬🇧 <b>{english_text}</b>\n\n"
        if transcription:
            text += f"📝 <code>{transcription}</code>\n\n"
        
        # Get audio media
        teacher_media = await audio_service.get_teacher_media(card.card_id, card.user_id)
        actor_media = await audio_service.get_actor_media(card.card_id, card.user_id)
        
        # Determine which audio to show and build audio status text
        if current_audio == "teacher" and teacher_media:
            audio_media = teacher_media
            audio_status = "🎧 Сейчас играет: Голос преподавателя"
        elif current_audio == "actor" and actor_media:
            audio_media = actor_media
            audio_status = "🎭 Сейчас играет: Голос актера"
        elif teacher_media:
            audio_media = teacher_media
            audio_status = "🎧 Сейчас играет: Голос преподавателя"
            current_audio = "teacher"
        elif actor_media:
            audio_media = actor_media
            audio_status = "🎭 Сейчас играет: Голос актера"
            current_audio = "actor"
        else:
            audio_media = None
            audio_status = "🔇 Аудио будет добавлено позже"
        
        text += f"{audio_status}\n\n"
        text += "🧠 Оцените, насколько хорошо вы знали выражение:"
        
        # Create keyboard with audio switching and evaluation buttons
        keyboard = self._get_answer_keyboard_with_audio_switch(card.card_id, current_audio, bool(teacher_media), bool(actor_media))
        
        logger.info(f"Created keyboard for card {card.card_id}, current_audio: {current_audio}, has_teacher: {bool(teacher_media)}, has_actor: {bool(actor_media)}")
        
        # Render with or without audio
        if audio_media:
            # One audio with switching capability
            await self._edit_message_with_audio(message_or_callback, audio_media, text, keyboard)
        else:
            # No audio available
            await self._edit_message(message_or_callback, text, keyboard)
        
        logger.info(f"Rendered answer for card {card.card_id}, user {card.user_id}, audio: {current_audio}")
    
    async def render_completion_message(self, message_or_callback: Union[Message, CallbackQuery], 
                                      message_type: str) -> None:
        """Render completion messages (learning finished, review finished)"""
        if message_type == "learning_completed":
            text = ("🎉 <b>Поздравляю!</b>\n\n"
                   "Вы завершили фазу обучения!\n"
                   "Теперь карточки будут показываться по расписанию "
                   "в соответствии с алгоритмом интервального повторения.\n\n"
                   "Я буду присылать вам напоминания, когда придет время повторить карточки.")
        elif message_type == "review_completed":
            text = ("✅ <b>Отлично!</b>\n\n"
                   "Вы повторили все карточки на сегодня.\n"
                   "Я напомню вам, когда придет время для следующего повторения!")
        else:
            text = "✅ Обучение завершено! Теперь карточки будут показываться по расписанию."
        
        await self._edit_message(message_or_callback, text, None)
        logger.info(f"Rendered completion message: {message_type}")
    
    async def switch_audio(self, message_or_callback: Union[Message, CallbackQuery], 
                          card: UserCard, audio_type: str, session_state: SessionState) -> None:
        """Switch between teacher and actor audio in the same message"""
        # Re-render the answer with the new audio type
        await self.render_answer(message_or_callback, card, session_state, audio_type)
        logger.info(f"Switched to {audio_type} audio for card {card.card_id}")
    
    def _get_show_answer_keyboard(self, card_id: int) -> InlineKeyboardMarkup:
        """Create keyboard with 'Show answer' button"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👁 Показать ответ", callback_data=f"show_answer:{card_id}")]
        ])
    
    def _get_answer_keyboard(self, card_id: int, has_teacher: bool, has_actor: bool) -> InlineKeyboardMarkup:
        """Create keyboard with audio buttons and evaluation buttons"""
        keyboard_rows = []
        
        # Add audio buttons if both are available
        if has_teacher and has_actor:
            keyboard_rows.append([
                InlineKeyboardButton(text="🎧 Преподаватель", callback_data=f"audio_teacher:{card_id}"),
                InlineKeyboardButton(text="🎭 Актер", callback_data=f"audio_actor:{card_id}"),
            ])
        
        # Add evaluation buttons
        keyboard_rows.append([
            InlineKeyboardButton(text="✅ Знал", callback_data=f"knew:{card_id}"),
            InlineKeyboardButton(text="🤔 Сомневался", callback_data=f"uncertain:{card_id}"),
            InlineKeyboardButton(text="❌ Не знал", callback_data=f"forgot:{card_id}"),
        ])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    def _get_answer_keyboard_with_audio_switch(self, card_id: int, current_audio: str, has_teacher: bool, has_actor: bool) -> InlineKeyboardMarkup:
        """Create keyboard with audio switching and evaluation buttons"""
        keyboard_rows = []
        
        # Add audio switching button if both are available
        if has_teacher and has_actor:
            if current_audio == "teacher":
                switch_button = InlineKeyboardButton(text="🔄 Переключить на актера", callback_data=f"switch_audio:{card_id}:actor")
            else:
                switch_button = InlineKeyboardButton(text="🔄 Переключить на преподавателя", callback_data=f"switch_audio:{card_id}:teacher")
            keyboard_rows.append([switch_button])
        
        # Add evaluation buttons in one row
        keyboard_rows.append([
            InlineKeyboardButton(text="✅", callback_data=f"knew:{card_id}"),
            InlineKeyboardButton(text="🤔", callback_data=f"uncertain:{card_id}"),
            InlineKeyboardButton(text="❌", callback_data=f"forgot:{card_id}"),
        ])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    async def _edit_message(self, message_or_callback: Union[Message, CallbackQuery], 
                          text: str, keyboard: Optional[InlineKeyboardMarkup]) -> None:
        """Edit message with text content"""
        message = message_or_callback.message if isinstance(message_or_callback, CallbackQuery) else message_or_callback
        
        # Check if current message has media (audio, video, etc.)
        if message.audio or message.video or message.photo or message.document:
            # If message has media, we need to delete it first and send new text message
            # But since we want to keep the same message, we'll use edit_caption for media messages
            if message.audio:
                # For audio messages, we can't edit to text, so we need to delete and resend
                await message.delete()
                if isinstance(message_or_callback, CallbackQuery):
                    new_message = await message_or_callback.message.answer(
                        text, 
                        reply_markup=keyboard, 
                        parse_mode="HTML"
                    )
                    # Update the callback message reference
                    message_or_callback.message = new_message
                else:
                    new_message = await message_or_callback.answer(
                        text, 
                        reply_markup=keyboard, 
                        parse_mode="HTML"
                    )
            else:
                # For other media types, try to edit caption
                await message.edit_caption(
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
        else:
            # Regular text message - can edit normally
            if isinstance(message_or_callback, CallbackQuery):
                await message_or_callback.message.edit_text(
                    text, 
                    reply_markup=keyboard, 
                    parse_mode="HTML"
                )
            else:
                await message_or_callback.edit_text(
                    text, 
                    reply_markup=keyboard, 
                    parse_mode="HTML"
                )
    
    async def _edit_message_with_audio(self, message_or_callback: Union[Message, CallbackQuery], 
                                     audio_media: InputMediaAudio, text: str, 
                                     keyboard: Optional[InlineKeyboardMarkup]) -> None:
        """Edit message with audio content"""
        # Create new InputMediaAudio with caption
        from aiogram.types import InputMediaAudio
        new_audio_media = InputMediaAudio(
            media=audio_media.media,
            caption=text,
            parse_mode="HTML"
        )
        
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_media(
                media=new_audio_media,
                reply_markup=keyboard
            )
        else:
            await message_or_callback.edit_media(
                media=new_audio_media,
                reply_markup=keyboard
            )
    
    async def _show_audio_placeholder(self, message_or_callback: Union[Message, CallbackQuery], 
                                    message: str) -> None:
        """Show audio placeholder message"""
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.answer(message, show_alert=True)
        else:
            # For Message, we can't show alert, so just log
            logger.info(f"Audio placeholder: {message}")


# Global card view renderer instance
card_view_renderer = CardViewRenderer()
