from typing import Union, Optional
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAudio
from aiogram.exceptions import TelegramBadRequest
from services.training_service import training_service
from services.audio_service import audio_service
from storage.json_storage import storage
import logging

logger = logging.getLogger(__name__)

class TrainingViewRenderer:
    """Renders training mode UI with two fixed messages: list and card"""
    
    async def render_list(self, message_or_callback: Union[Message, CallbackQuery], 
                         page: int, user_id: int) -> None:
        """Display or update phrase list"""
        user = await storage.get_user(user_id)
        if not user:
            logger.error(f"User {user_id} not found for training list")
            return
        
        text = training_service.format_list_text(page)
        keyboard = training_service.create_list_keyboard(page)
        
        try:
            if user.training_list_message_id:
                # Try to edit existing message
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
                logger.info(f"Updated training list for user {user_id}, page {page}")
            else:
                # Send new message
                if isinstance(message_or_callback, CallbackQuery):
                    new_message = await message_or_callback.message.answer(
                        text, 
                        reply_markup=keyboard, 
                        parse_mode="HTML"
                    )
                else:
                    new_message = await message_or_callback.answer(
                        text, 
                        reply_markup=keyboard, 
                        parse_mode="HTML"
                    )
                
                # Store message ID
                user.training_list_message_id = new_message.message_id
                await storage.save_user(user)
                logger.info(f"Created new training list for user {user_id}, page {page}")
                
        except TelegramBadRequest as e:
            logger.warning(f"Failed to edit training list for user {user_id}: {e}")
            # Send new message and update ID
            if isinstance(message_or_callback, CallbackQuery):
                new_message = await message_or_callback.message.answer(
                    text, 
                    reply_markup=keyboard, 
                    parse_mode="HTML"
                )
            else:
                new_message = await message_or_callback.answer(
                    text, 
                    reply_markup=keyboard, 
                    parse_mode="HTML"
                )
            
            user.training_list_message_id = new_message.message_id
            await storage.save_user(user)
            logger.info(f"Recreated training list for user {user_id}, page {page}")
    
    async def render_card(self, message_or_callback: Union[Message, CallbackQuery], 
                         card_id: int, user_id: int, audio_type: str) -> None:
        """Display or update training card with single switchable audio player"""
        user = await storage.get_user(user_id)
        if not user:
            logger.error(f"User {user_id} not found for training card")
            return
        
        phrase = training_service.get_card_by_id(card_id)
        if not phrase:
            logger.error(f"Phrase {card_id} not found")
            return
        
        position = training_service.get_card_position(card_id)
        english_text = phrase["text_en"]
        transcription = phrase.get("transcription", "")
        
        # Build card text
        text = f"Фраза {position}/22 (тренировка)\n\n"
        text += f"🇬🇧 {english_text}\n"
        if transcription:
            text += f"📖 {transcription}\n"
        text += "\n"
        
        # Get audio media
        teacher_media = await audio_service.get_teacher_media(card_id, user_id)
        actor_media = await audio_service.get_actor_media(card_id, user_id)
        
        # Determine current audio and status text
        if audio_type == "teacher" and teacher_media:
            current_media = teacher_media
            audio_status = "🎧 Сейчас: Преподаватель"
            has_current_audio = True
        elif audio_type == "actor" and actor_media:
            current_media = actor_media
            audio_status = "🎭 Сейчас: Актёр"
            has_current_audio = True
        elif teacher_media:  # Fallback to teacher
            current_media = teacher_media
            audio_status = "🎧 Сейчас: Преподаватель"
            has_current_audio = True
            audio_type = "teacher"
        elif actor_media:  # Fallback to actor
            current_media = actor_media
            audio_status = "🎭 Сейчас: Актёр"
            has_current_audio = True
            audio_type = "actor"
        else:
            current_media = None
            audio_status = "🔇 аудио будет добавлено позже"
            has_current_audio = False
        
        text += f"{audio_status}\n"
        
        # Create keyboard
        keyboard = self._create_card_keyboard(card_id, audio_type, bool(teacher_media), bool(actor_media))
        
        try:
            if user.training_card_message_id:
                # Try to edit existing message
                if has_current_audio and current_media:
                    # Edit with audio
                    new_audio_media = InputMediaAudio(
                        media=current_media.media,
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
                else:
                    # Edit text only
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
                logger.info(f"Updated training card for user {user_id}, card {card_id}, audio: {audio_type}")
            else:
                # Send new message
                if has_current_audio and current_media:
                    # Send with audio
                    if isinstance(message_or_callback, CallbackQuery):
                        new_message = await message_or_callback.message.answer_audio(
                            audio=current_media.media,
                            caption=text,
                            reply_markup=keyboard,
                            parse_mode="HTML"
                        )
                    else:
                        new_message = await message_or_callback.answer_audio(
                            audio=current_media.media,
                            caption=text,
                            reply_markup=keyboard,
                            parse_mode="HTML"
                        )
                else:
                    # Send text only
                    if isinstance(message_or_callback, CallbackQuery):
                        new_message = await message_or_callback.message.answer(
                            text,
                            reply_markup=keyboard,
                            parse_mode="HTML"
                        )
                    else:
                        new_message = await message_or_callback.answer(
                            text,
                            reply_markup=keyboard,
                            parse_mode="HTML"
                        )
                
                # Store message ID
                user.training_card_message_id = new_message.message_id
                await storage.save_user(user)
                logger.info(f"Created new training card for user {user_id}, card {card_id}, audio: {audio_type}")
                
        except TelegramBadRequest as e:
            logger.warning(f"Failed to edit training card for user {user_id}: {e}")
            # Send new message and update ID
            if has_current_audio and current_media:
                if isinstance(message_or_callback, CallbackQuery):
                    new_message = await message_or_callback.message.answer_audio(
                        audio=current_media.media,
                        caption=text,
                        reply_markup=keyboard,
                        parse_mode="HTML"
                    )
                else:
                    new_message = await message_or_callback.answer_audio(
                        audio=current_media.media,
                        caption=text,
                        reply_markup=keyboard,
                        parse_mode="HTML"
                    )
            else:
                if isinstance(message_or_callback, CallbackQuery):
                    new_message = await message_or_callback.message.answer(
                        text,
                        reply_markup=keyboard,
                        parse_mode="HTML"
                    )
                else:
                    new_message = await message_or_callback.answer(
                        text,
                        reply_markup=keyboard,
                        parse_mode="HTML"
                    )
            
            user.training_card_message_id = new_message.message_id
            await storage.save_user(user)
            logger.info(f"Recreated training card for user {user_id}, card {card_id}, audio: {audio_type}")
    
    async def close_card(self, message_or_callback: Union[Message, CallbackQuery], user_id: int) -> None:
        """Close training card by deleting the message"""
        user = await storage.get_user(user_id)
        if not user or not user.training_card_message_id:
            return
        
        try:
            if isinstance(message_or_callback, CallbackQuery):
                await message_or_callback.message.delete()
            else:
                await message_or_callback.delete()
            
            # Clear card message ID
            user.training_card_message_id = None
            user.training_selected_card_id = None
            await storage.save_user(user)
            logger.info(f"Closed training card for user {user_id}")
            
        except TelegramBadRequest as e:
            logger.warning(f"Failed to delete training card for user {user_id}: {e}")
            # Clear IDs anyway
            user.training_card_message_id = None
            user.training_selected_card_id = None
            await storage.save_user(user)
    
    def _create_card_keyboard(self, card_id: int, current_audio: str, 
                             has_teacher: bool, has_actor: bool) -> InlineKeyboardMarkup:
        """Create keyboard for training card"""
        keyboard_rows = []
        
        # Add audio switching button if both are available
        if has_teacher and has_actor:
            if current_audio == "teacher":
                switch_button = InlineKeyboardButton(
                    text="🔄 Переключить на актёра",
                    callback_data=f"tr:switch:id={card_id}:from={current_audio}"
                )
            else:
                switch_button = InlineKeyboardButton(
                    text="🔄 Переключить на преподавателя",
                    callback_data=f"tr:switch:id={card_id}:from={current_audio}"
                )
            keyboard_rows.append([switch_button])
        
        # Add close button
        keyboard_rows.append([
            InlineKeyboardButton(
                text="🔙 Вернуться к списку",
                callback_data="tr:close"
            )
        ])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)

# Global training view renderer instance
training_view_renderer = TrainingViewRenderer()
