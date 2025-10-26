from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.group_stats_service import group_stats_service


router = Router()


@router.message(Command("group_stats"))
async def cmd_group_stats(message: Message):
    """Handle /group_stats command"""
    
    stats = await group_stats_service.get_group_stats()
    
    if not stats or not stats['users']:
        await message.answer(
            "📊 Пока нет других пользователей в системе.",
            parse_mode="HTML"
        )
        return
    
    # Build table header
    text = "📊 <b>Статистика группы:</b>\n\n"
    text += "<code>"
    text += "Пользователь       Изучено/Всего  Ожидает  Стрик\n"
    text += "─" * 55 + "\n"
    
    # Build table rows
    for user in stats['users']:
        # Truncate name to fit in table
        name = user['display_name'][:15].ljust(15)
        learned_total = f"{user['learned']}/{user['total']}".ljust(13)
        due = str(user['due']).ljust(7)
        streak = f"{user['streak']} дн."
        
        text += f"{name}  {learned_total}  {due}  {streak}\n"
    
    text += "</code>\n"
    
    # Summary
    text += f"\n📈 <b>Итого:</b>\n"
    text += f"Всего пользователей: {stats['total_users']}\n"
    text += f"Средний прогресс: {stats['avg_progress']:.1f}%"
    
    await message.answer(text, parse_mode="HTML")

