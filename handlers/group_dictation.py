from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from config import DEFAULT_PHRASES
from services.audio_service import audio_service
import logging

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("group_show:"))
async def show_group_answer(callback: CallbackQuery):
    """Show answer for group dictation card"""
    try:
        # Parse phrase ID from callback data
        phrase_id = int(callback.data.split(":")[1])
        
        # Find phrase in DEFAULT_PHRASES
        phrase = next((p for p in DEFAULT_PHRASES if p['id'] == phrase_id), None)
        
        if not phrase:
            await callback.answer("❌ Фраза не найдена")
            return
        
        logger.info(f"Group answer requested for phrase {phrase_id}")
        
        # Format answer text
        text = f"🎯 <b>Диктант</b> - Фраза {phrase['id']}/22\n\n"
        text += f"🇷🇺 <i>{phrase['text_ru']}</i>\n\n"
        text += f"🇬🇧 <b>{phrase['text_en']}</b>\n"
        text += f"📖 <code>{phrase['transcription']}</code>\n\n"
        text += f"🎧 Аудио: Преподаватель"
        
        # Try to get audio file
        audio_file = audio_service.get_audio_file_path(phrase['audio_teacher'])
        
        if audio_file:
            try:
                # Create keyboard with audio switch button
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="🔄 Переключить на актёра", 
                        callback_data=f"group_switch:{phrase_id}:actor"
                    )]
                ])
                
                # Send audio with text as caption
                audio = FSInputFile(audio_file)
                await callback.message.edit_media(
                    media={"type": "audio", "media": audio, "caption": text, "parse_mode": "HTML"},
                    reply_markup=keyboard
                )
                
                logger.info(f"Sent answer with audio for phrase {phrase_id}")
                
            except Exception as e:
                logger.error(f"Failed to send audio: {e}")
                # Fallback: edit text without audio
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔇 Аудио недоступно", callback_data="noop")]
                ])
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        else:
            # No audio file - just show text
            text += "\n\n🔇 <i>Аудио будет добавлено позже</i>"
            await callback.message.edit_text(text, parse_mode="HTML")
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error in show_group_answer: {e}")
        await callback.answer("❌ Ошибка при показе ответа")


@router.callback_query(F.data.startswith("group_switch:"))
async def switch_group_audio(callback: CallbackQuery):
    """Switch audio between teacher and actor in group dictation"""
    try:
        # Parse callback data: group_switch:phrase_id:audio_type
        parts = callback.data.split(":")
        phrase_id = int(parts[1])
        current_audio = parts[2]  # "teacher" or "actor"
        
        # Find phrase
        phrase = next((p for p in DEFAULT_PHRASES if p['id'] == phrase_id), None)
        
        if not phrase:
            await callback.answer("❌ Фраза не найдена")
            return
        
        # Toggle audio type
        new_audio = "teacher" if current_audio == "actor" else "actor"
        audio_filename = phrase['audio_teacher'] if new_audio == "teacher" else phrase['audio_actor']
        audio_label = "Преподаватель" if new_audio == "teacher" else "Актёр"
        button_text = "🔄 Переключить на актёра" if new_audio == "teacher" else "🔄 Переключить на преподавателя"
        
        logger.info(f"Switching audio for phrase {phrase_id} to {new_audio}")
        
        # Format text
        text = f"🎯 <b>Диктант</b> - Фраза {phrase['id']}/22\n\n"
        text += f"🇷🇺 <i>{phrase['text_ru']}</i>\n\n"
        text += f"🇬🇧 <b>{phrase['text_en']}</b>\n"
        text += f"📖 <code>{phrase['transcription']}</code>\n\n"
        text += f"🎧 Аудио: {audio_label}"
        
        # Get audio file
        audio_file = audio_service.get_audio_file_path(audio_filename)
        
        if audio_file:
            try:
                # Create keyboard for next toggle
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text=button_text,
                        callback_data=f"group_switch:{phrase_id}:{new_audio}"
                    )]
                ])
                
                # Edit message with new audio
                audio = FSInputFile(audio_file)
                await callback.message.edit_media(
                    media={"type": "audio", "media": audio, "caption": text, "parse_mode": "HTML"},
                    reply_markup=keyboard
                )
                
                # Show feedback
                if new_audio == "teacher":
                    await callback.answer("🎧 Переключено на голос преподавателя")
                else:
                    await callback.answer("🎭 Переключено на голос актёра")
                
                logger.info(f"Switched to {new_audio} audio for phrase {phrase_id}")
                
            except Exception as e:
                logger.error(f"Failed to switch audio: {e}")
                await callback.answer("❌ Ошибка переключения аудио")
        else:
            await callback.answer("🔇 Аудио недоступно")
        
    except Exception as e:
        logger.error(f"Error in switch_group_audio: {e}")
        await callback.answer("❌ Ошибка")

