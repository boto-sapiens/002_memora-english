from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.card_manager import card_manager
from services.session_manager import session_manager
from services.card_view_renderer import card_view_renderer
import logging

router = Router()
logger = logging.getLogger(__name__)


async def show_next_card(callback: CallbackQuery, telegram_id: int):
    """Show next card or completion message"""
    logger.info(f"show_next_card called for user {telegram_id}")
    
    # Get session state
    session_state = await session_manager.get_session_state(telegram_id)
    logger.info(f"Session state: {session_state}")
    
    if not session_state or session_state.is_completed:
        # Session completed
        logger.info(f"Session completed for user {telegram_id}")
        if session_state and session_state.phase == 'learning':
            await card_view_renderer.render_completion_message(callback, "learning_completed")
        else:
            await card_view_renderer.render_completion_message(callback, "review_completed")
        return
    
    # Get next card
    card = await session_manager.get_next_card(telegram_id)
    logger.info(f"Next card: {card.card_id if card else None}")
    
    if card:
        # Increment session index
        await session_manager.increment_session_index(telegram_id)
        logger.info(f"Session index incremented for user {telegram_id}")
        
        # Get updated session state
        updated_session_state = await session_manager.get_session_state(telegram_id)
        logger.info(f"Updated session state: {updated_session_state}")
        
        # Render question phase
        await card_view_renderer.render_question(callback, card, updated_session_state)
        logger.info(f"Question rendered for card {card.card_id}")
    else:
        # No more cards in session
        logger.info(f"No more cards in session for user {telegram_id}")
        if session_state.phase == 'learning':
            await card_view_renderer.render_completion_message(callback, "learning_completed")
        else:
            await card_view_renderer.render_completion_message(callback, "review_completed")


@router.callback_query(F.data.startswith("knew:"))
async def handle_knew(callback: CallbackQuery):
    """Handle 'knew' response"""
    telegram_id = callback.from_user.id
    card_id = int(callback.data.split(":")[1])
    
    logger.info(f"handle_knew called for user {telegram_id}, card {card_id}")
    
    # Process response
    await card_manager.process_response(telegram_id, card_id, "knew")
    logger.info(f"Response processed for card {card_id}")
    
    # Show next card
    await show_next_card(callback, telegram_id)
    await callback.answer("✅ Отлично!")
    logger.info(f"Next card shown for user {telegram_id}")


@router.callback_query(F.data.startswith("uncertain:"))
async def handle_uncertain(callback: CallbackQuery):
    """Handle 'uncertain' response"""
    telegram_id = callback.from_user.id
    card_id = int(callback.data.split(":")[1])
    
    # Process response
    await card_manager.process_response(telegram_id, card_id, "uncertain")
    
    # Show next card
    await show_next_card(callback, telegram_id)
    await callback.answer("🤔 Хорошо!")


@router.callback_query(F.data.startswith("forgot:"))
async def handle_forgot(callback: CallbackQuery):
    """Handle 'forgot' response"""
    telegram_id = callback.from_user.id
    card_id = int(callback.data.split(":")[1])
    
    # Process response
    await card_manager.process_response(telegram_id, card_id, "forgot")
    
    # Show next card
    await show_next_card(callback, telegram_id)
    await callback.answer("❌ Ничего страшного, повторим!")