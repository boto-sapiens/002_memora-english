"""Arena dictation control handlers."""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import logging
import json
import os

router = Router()
logger = logging.getLogger(__name__)

# Path to control file
CONTROL_FILE = "data/arena_control.json"


def load_arena_state():
    """Load arena dictation state from file."""
    if os.path.exists(CONTROL_FILE):
        try:
            with open(CONTROL_FILE, 'r') as f:
                data = json.load(f)
                return data.get('dictation_enabled', True)
        except Exception as e:
            logger.error(f"Error loading arena state: {e}")
    return True  # Default: enabled


def save_arena_state(enabled: bool):
    """Save arena dictation state to file."""
    try:
        os.makedirs(os.path.dirname(CONTROL_FILE), exist_ok=True)
        with open(CONTROL_FILE, 'w') as f:
            json.dump({'dictation_enabled': enabled}, f)
        logger.info(f"Arena state saved: enabled={enabled}")
        return True
    except Exception as e:
        logger.error(f"Error saving arena state: {e}")
        return False


@router.message(Command("arena_on"))
async def arena_dictation_on(message: Message):
    """Enable arena dictation."""
    success = save_arena_state(True)
    if success:
        await message.answer(
            "✅ <b>Arena dictation включена!</b>\n\n"
            "Memora-English будет отправлять фразы в Arena каждую минуту.\n"
            "ChroniclerBot будет генерировать AI ответы (расход токенов OpenAI).\n\n"
            "📊 Команды:\n"
            "/arena_off - отключить\n"
            "/arena_status - проверить статус"
        )
    else:
        await message.answer("❌ Ошибка сохранения настроек")


@router.message(Command("arena_off"))
async def arena_dictation_off(message: Message):
    """Disable arena dictation."""
    success = save_arena_state(False)
    if success:
        await message.answer(
            "🛑 <b>Arena dictation выключена!</b>\n\n"
            "Memora-English НЕ будет отправлять фразы в Arena.\n"
            "Экономия токенов OpenAI.\n\n"
            "📊 Команды:\n"
            "/arena_on - включить\n"
            "/arena_status - проверить статус"
        )
    else:
        await message.answer("❌ Ошибка сохранения настроек")


@router.message(Command("arena_status"))
async def arena_dictation_status(message: Message):
    """Show arena dictation status."""
    enabled = load_arena_state()
    
    status_icon = "✅" if enabled else "🛑"
    status_text = "Включена" if enabled else "Выключена"
    
    from config import ARENA_URL, ARENA_ENABLED, TARGET_CHAT_ID
    
    response = (
        f"📊 <b>Arena Dictation Status</b>\n\n"
        f"{status_icon} <b>Статус:</b> {status_text}\n"
        f"🔗 <b>Arena URL:</b> {ARENA_URL}\n"
        f"🎯 <b>Target Chat:</b> {TARGET_CHAT_ID}\n"
        f"⚙️ <b>Config enabled:</b> {ARENA_ENABLED}\n\n"
    )
    
    if enabled:
        response += (
            "💡 <b>Активно:</b> Фразы отправляются каждую минуту\n"
            "💰 <b>Токены:</b> Расходуются (ChroniclerBot AI)\n\n"
            "📊 Команды:\n"
            "/arena_off - выключить для экономии токенов"
        )
    else:
        response += (
            "💡 <b>Пауза:</b> Фразы НЕ отправляются\n"
            "💰 <b>Токены:</b> Не расходуются\n\n"
            "📊 Команды:\n"
            "/arena_on - включить отправку"
        )
    
    # Add control buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Включить" if not enabled else "🛑 Выключить",
                callback_data="arena_toggle"
            ),
            InlineKeyboardButton(
                text="🔄 Обновить",
                callback_data="arena_refresh"
            )
        ]
    ])
    
    await message.answer(response, reply_markup=keyboard)


@router.callback_query(F.data == "arena_toggle")
async def arena_toggle_callback(callback: CallbackQuery):
    """Toggle arena dictation via callback."""
    current_state = load_arena_state()
    new_state = not current_state
    
    success = save_arena_state(new_state)
    
    if success:
        status_text = "включена" if new_state else "выключена"
        await callback.answer(f"Arena dictation {status_text}!", show_alert=True)
        
        # Refresh status display
        await arena_dictation_status(callback.message)
    else:
        await callback.answer("Ошибка изменения статуса", show_alert=True)


@router.callback_query(F.data == "arena_refresh")
async def arena_refresh_callback(callback: CallbackQuery):
    """Refresh arena status display."""
    await callback.answer("Статус обновлен")
    await arena_dictation_status(callback.message)

