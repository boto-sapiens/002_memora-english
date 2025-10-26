from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from storage.json_storage import storage
from services.card_manager import card_manager
from services.session_manager import session_manager
from services.card_view_renderer import card_view_renderer
import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command"""
    telegram_id = message.from_user.id
    username = message.from_user.username
    
    # Check if user exists
    user = await storage.get_user(telegram_id)
    
    if not user:
        # New user - start learning phase
        await card_manager.start_learning_phase(telegram_id, username)
        await session_manager.initialize_learning_session(telegram_id)
        
        # Get first card and session state
        card = await session_manager.get_next_card(telegram_id)
        session_state = await session_manager.get_session_state(telegram_id)
        
        if card and session_state:
            # Send initial message for new user
            russian_text = card.text_ru if card.text_ru else card.text
            progress_text = f"📊 Прогресс: {session_state.current_index + 1}/{session_state.total_in_session}"
            text = f"{progress_text}\n\n🇷🇺 <i>{russian_text}</i>"
            
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👁 Показать ответ", callback_data=f"show_answer:{card.card_id}")]
            ])
            
            await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        else:
            await message.answer("❌ Ошибка инициализации. Попробуйте еще раз.")
    else:
        # Existing user
        if not user.learning_phase_completed:
            # Continue learning phase
            card = await session_manager.get_next_card(telegram_id)
            session_state = await session_manager.get_session_state(telegram_id)
            
            if card and session_state:
                # Send message for existing user
                russian_text = card.text_ru if card.text_ru else card.text
                progress_text = f"📊 Прогресс: {session_state.current_index + 1}/{session_state.total_in_session}"
                text = f"{progress_text}\n\n🇷🇺 <i>{russian_text}</i>"
                
                from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="👁 Показать ответ", callback_data=f"show_answer:{card.card_id}")]
                ])
                
                await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
            else:
                await message.answer("✅ Обучение завершено! Теперь карточки будут показываться по расписанию.")
        else:
            # Start review phase
            # Сбросить старую сессию
            await session_manager.reset_session(telegram_id)
            
            card = await session_manager.get_next_card(telegram_id)
            session_state = await session_manager.get_session_state(telegram_id)
            
            if card and session_state:
                # Инициализировать новую сессию review
                user = await storage.get_user(telegram_id)
                if user:
                    user.current_session_index = 0
                    await storage.save_user(user)
                
                # Send message for review
                russian_text = card.text_ru if card.text_ru else card.text
                progress_text = f"📊 Прогресс: {session_state.current_index + 1}/{session_state.total_in_session}"
                text = f"{progress_text}\n\n🇷🇺 <i>{russian_text}</i>"
                
                from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="👁 Показать ответ", callback_data=f"show_answer:{card.card_id}")]
                ])
                
                await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
            else:
                await message.answer("✅ Нет карточек для повторения!")


@router.callback_query(F.data.startswith("show_answer:"))
async def show_answer(callback: CallbackQuery):
    """Show answer phase of the card"""
    telegram_id = callback.from_user.id
    card_id = int(callback.data.split(":")[1])
    
    logger.info(f"show_answer called for user {telegram_id}, card {card_id}")
    
    # Get card and session state
    cards = await storage.get_user_cards(telegram_id)
    card = next((c for c in cards if c.card_id == card_id), None)
    session_state = await session_manager.get_session_state(telegram_id)
    
    logger.info(f"Found card: {card is not None}, session_state: {session_state is not None}")
    
    if not card or not session_state:
        logger.warning(f"Card or session state not found for user {telegram_id}")
        await callback.answer("❌ Карточка не найдена")
        return
    
    # Render answer phase with teacher audio by default
    logger.info(f"Rendering answer for card {card_id}")
    await card_view_renderer.render_answer(callback, card, session_state, "teacher")
    await callback.answer()
    logger.info(f"Answer rendered successfully for card {card_id}")


@router.callback_query(F.data.startswith("switch_audio:"))
async def switch_audio(callback: CallbackQuery):
    """Switch between teacher and actor audio"""
    telegram_id = callback.from_user.id
    parts = callback.data.split(":")
    card_id = int(parts[1])
    audio_type = parts[2]  # "teacher" or "actor"
    
    logger.info(f"switch_audio called for user {telegram_id}, card {card_id}, audio_type: {audio_type}")
    
    # Get card and session state
    cards = await storage.get_user_cards(telegram_id)
    card = next((c for c in cards if c.card_id == card_id), None)
    session_state = await session_manager.get_session_state(telegram_id)
    
    logger.info(f"Found card: {card is not None}, session_state: {session_state is not None}")
    
    if not card or not session_state:
        logger.warning(f"Card or session state not found for user {telegram_id}")
        await callback.answer("❌ Карточка не найдена")
        return
    
    # Switch audio
    logger.info(f"Switching to {audio_type} audio for card {card_id}")
    await card_view_renderer.switch_audio(callback, card, audio_type, session_state)
    
    # Show feedback
    if audio_type == "teacher":
        await callback.answer("🎧 Переключено на голос преподавателя")
    else:
        await callback.answer("🎭 Переключено на голос актера")
    
    logger.info(f"Audio switch completed for card {card_id}, audio_type: {audio_type}")