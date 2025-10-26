from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from storage.json_storage import storage
from services.training_service import training_service
from services.training_view_renderer import training_view_renderer
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("training"))
async def cmd_training(message: Message):
    """Handle /training command - initialize training mode"""
    telegram_id = message.from_user.id
    username = message.from_user.username
    
    logger.info(f"Training command from user {telegram_id}")
    
    # Get or create user
    user = await storage.get_user(telegram_id)
    if not user:
        # Create new user (minimal setup for training)
        from datetime import datetime
        user = await storage.create_user(telegram_id, username)
    
    # Clear any existing card
    if user.training_card_message_id:
        user.training_card_message_id = None
        user.training_selected_card_id = None
        await storage.save_user(user)
    
    # Set to page 1
    user.training_current_page = 1
    await storage.save_user(user)
    
    # Render list (page 1)
    await training_view_renderer.render_list(message, 1, telegram_id)
    logger.info(f"Training mode initialized for user {telegram_id}")

@router.callback_query(F.data.startswith("tr:item:"))
async def handle_phrase_selection(callback: CallbackQuery):
    """Handle phrase selection from list"""
    telegram_id = callback.from_user.id
    
    # Parse callback data: tr:item:id={card_id}:p={page}
    try:
        parts = callback.data.split(":")
        card_id_part = parts[2]  # id={card_id}
        page_part = parts[3]     # p={page}
        
        card_id = int(card_id_part.split("=")[1])
        page = int(page_part.split("=")[1])
        
        logger.info(f"Phrase selection: user {telegram_id}, card {card_id}, page {page}")
        
    except (IndexError, ValueError) as e:
        logger.error(f"Failed to parse phrase selection callback: {callback.data}, error: {e}")
        await callback.answer("❌ Ошибка выбора фразы")
        return
    
    # Get user and update state
    user = await storage.get_user(telegram_id)
    if not user:
        await callback.answer("❌ Пользователь не найден")
        return
    
    # Update user state
    user.training_selected_card_id = card_id
    user.training_current_audio = "teacher"  # Default to teacher
    await storage.save_user(user)
    
    # Render card
    await training_view_renderer.render_card(callback, card_id, telegram_id, "teacher")
    await callback.answer()
    logger.info(f"Rendered training card for user {telegram_id}, card {card_id}")

@router.callback_query(F.data.startswith("tr:page:"))
async def handle_page_navigation(callback: CallbackQuery):
    """Handle page navigation (prev/next)"""
    telegram_id = callback.from_user.id
    
    # Parse callback data: tr:page:prev:p={page} or tr:page:next:p={page}
    try:
        parts = callback.data.split(":")
        direction = parts[2]  # prev or next
        page_part = parts[3]  # p={page}
        
        current_page = int(page_part.split("=")[1])
        
        logger.info(f"Page navigation: user {telegram_id}, direction {direction}, current page {current_page}")
        
    except (IndexError, ValueError) as e:
        logger.error(f"Failed to parse page navigation callback: {callback.data}, error: {e}")
        await callback.answer("❌ Ошибка навигации")
        return
    
    # Calculate new page
    if direction == "prev":
        new_page = current_page - 1
    elif direction == "next":
        new_page = current_page + 1
    else:
        await callback.answer("❌ Неверное направление")
        return
    
    # Validate page bounds
    total_pages = training_service.get_total_pages()
    if new_page < 1 or new_page > total_pages:
        await callback.answer("❌ Неверная страница")
        return
    
    # Get user and update state
    user = await storage.get_user(telegram_id)
    if not user:
        await callback.answer("❌ Пользователь не найден")
        return
    
    # Update user state
    user.training_current_page = new_page
    await storage.save_user(user)
    
    # Update list
    await training_view_renderer.render_list(callback, new_page, telegram_id)
    await callback.answer()
    logger.info(f"Updated training list for user {telegram_id}, page {new_page}")

@router.callback_query(F.data.startswith("tr:switch:"))
async def handle_audio_switch(callback: CallbackQuery):
    """Handle audio switching in training card"""
    telegram_id = callback.from_user.id
    
    # Parse callback data: tr:switch:id={card_id}:from={current_audio}
    try:
        parts = callback.data.split(":")
        card_id_part = parts[2]  # id={card_id}
        audio_part = parts[3]    # from={current_audio}
        
        card_id = int(card_id_part.split("=")[1])
        current_audio = audio_part.split("=")[1]
        
        logger.info(f"Audio switch: user {telegram_id}, card {card_id}, from {current_audio}")
        
    except (IndexError, ValueError) as e:
        logger.error(f"Failed to parse audio switch callback: {callback.data}, error: {e}")
        await callback.answer("❌ Ошибка переключения аудио")
        return
    
    # Get user and update state
    user = await storage.get_user(telegram_id)
    if not user:
        await callback.answer("❌ Пользователь не найден")
        return
    
    # Toggle audio type
    new_audio = "actor" if current_audio == "teacher" else "teacher"
    user.training_current_audio = new_audio
    await storage.save_user(user)
    
    # Re-render card with new audio
    await training_view_renderer.render_card(callback, card_id, telegram_id, new_audio)
    
    # Show feedback
    if new_audio == "teacher":
        await callback.answer("🎧 Переключено на голос преподавателя")
    else:
        await callback.answer("🎭 Переключено на голос актёра")
    
    logger.info(f"Switched audio for user {telegram_id}, card {card_id}, to {new_audio}")

@router.callback_query(F.data == "tr:close")
async def handle_close_card(callback: CallbackQuery):
    """Handle closing training card"""
    telegram_id = callback.from_user.id
    
    logger.info(f"Close card request from user {telegram_id}")
    
    # Close card
    await training_view_renderer.close_card(callback, telegram_id)
    await callback.answer("✅ Карточка закрыта")
    logger.info(f"Closed training card for user {telegram_id}")
