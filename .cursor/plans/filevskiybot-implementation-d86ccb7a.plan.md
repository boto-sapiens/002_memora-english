<!-- d86ccb7a-f4df-4f5c-9321-6953b3d00efa 923ad909-ea7b-46ec-9c1f-551113f35f89 -->
# Training Mode Implementation (Updated)

## Overview

Implement `/training` command that displays a paginated list of phrases (8 per page). When user selects a phrase, a card with ONE switchable audio player is displayed below the list. Both messages are fixed and always edited, never recreated.

## Architecture

### 1. Data Models (storage/models.py)

Add training session state to User model:

```python
# Add to User dataclass:
training_list_message_id: Optional[int] = None
training_card_message_id: Optional[int] = None
training_current_page: int = 1
training_selected_card_id: Optional[int] = None
training_current_audio: str = "teacher"  # "teacher" or "actor"
```

This ensures persistence and prevents race conditions. No separate in-memory dict needed.

### 2. Training Service (services/training_service.py)

Create service to handle:

- Paginated phrase list generation (8 cards per page)
- Page navigation logic with boundary checks
- Calculate total pages from DEFAULT_PHRASES length (22 cards = 3 pages)
- Format list text with phrase numbers and English titles

Key methods:

- `get_page_phrases(page: int) -> List[dict]` - returns phrases for given page (sliced from DEFAULT_PHRASES)
- `get_total_pages() -> int` - returns 3 (ceil(22/8))
- `format_list_text(page: int) -> str` - formats "📚 Тренировка (стр. X/Y)\n\n1. Phrase...\n2. Phrase..."
- `create_list_keyboard(page: int) -> InlineKeyboardMarkup` - creates phrase buttons + nav buttons with callback data `tr:item:id=X:p=Y` and `tr:page:prev:p=X` / `tr:page:next:p=X`
- `get_card_by_id(card_id: int) -> Optional[dict]` - returns phrase dict from DEFAULT_PHRASES

### 3. Training View Renderer (services/training_view_renderer.py)

Handle UI rendering with two fixed messages:

- Render paginated list (edit only, never send new)
- Render training card with ONE switchable audio player (edit only after first send)
- Use `edit_message_text` for list updates
- Use `edit_message_media` for card with audio, `edit_message_text` for card without audio

Key methods:

- `render_list(message_or_callback, page: int, user_id: int)` - displays/updates phrase list
  - If first time (no list_message_id), send message and store ID
  - Otherwise, edit existing message
- `render_card(message_or_callback, card_id: int, user_id: int, audio_type: str)` - displays training card
  - If first time (no card_message_id), send message and store ID
  - Otherwise, edit existing message with new card content
  - Show ONE audio player (teacher or actor based on audio_type)
  - Include audio switch button if both audios exist
  - Format: "Фраза X/22 (тренировка)\n\n🇬🇧 Text\n📖 Transcription\n\n🎧 Сейчас: Преподаватель"
  - If audio missing for current type, show text placeholder below: "🔇 аудио будет добавлено позже"
  - Bottom button: "🔙 Вернуться к списку" (callback: `tr:close`)

### 4. Handler (handlers/training.py)

Handle user interactions with structured callbacks:

- `/training` command - initialize training mode, render/update list to page 1
  - If user.training_list_message_id exists, try to edit it; if fails, send new and update ID
  - If user.training_card_message_id exists, clear it (delete message or ignore)
  - Set user.training_current_page = 1
- Callback `tr:item:id={card_id}:p={page}` - user selects phrase
  - Parse card_id and page from callback
  - Set user.training_selected_card_id = card_id
  - Set user.training_current_audio = "teacher" (default)
  - Render card below list
- Callback `tr:page:prev:p={page}` or `tr:page:next:p={page}` - navigate pages
  - Calculate new page (prev: page-1, next: page+1)
  - Update user.training_current_page
  - Edit list message with new page content
- Callback `tr:switch:id={card_id}:from={current_audio}` - switch audio
  - Toggle audio_type: teacher <-> actor
  - Update user.training_current_audio
  - Edit card message with new audio via `edit_message_media`
- Callback `tr:close` - close card
  - Delete card message or replace with instruction text
  - Clear user.training_card_message_id and user.training_selected_card_id
- All callbacks: use `answerCallbackQuery()` immediately
- Use user lock (save user after each operation) to prevent race conditions

Implementation flow:

1. `/training` -> edit or send list (page 1), store list_message_id
2. User clicks phrase -> send or edit card below, store card_message_id
3. User clicks pagination -> edit list message only
4. User clicks another phrase -> edit card message with new content
5. User clicks audio switch -> edit card message media (InputMediaAudio)
6. User clicks "Вернуться к списку" -> delete card message, clear card_message_id

### 5. Integration Points

**bot.py:**

- Import training handler: `from handlers import training`
- Register router: `dp.include_router(training.router)` (after start, before help)
- Add command to menu: `BotCommand(command="training", description="📚 Режим тренировки")`

**Training Card Format:**

```
Фраза X/22 (тренировка)

🇬🇧 English text
📖 transcription

🎧 Сейчас: Преподаватель
<audio player teacher via edit_message_media>

[🔄 Переключить на актёра]  (if both exist)
[🔙 Вернуться к списку]
```

If audio missing: show text placeholder "🔇 аудио будет добавлено позже"

**List Format:**

```
📚 Тренировка (стр. X/Y)

1. Charming day it has been, Miss Fairfax.
2. Pray don't talk to me about the weather, Mr. Worthing.
...
8. I would certainly advise you to do so.

[⬅ Назад] [➡ Вперёд]
```

Each phrase is an inline button with callback `tr:item:id={card_id}:p={page}`

## Implementation Steps

1. Update `storage/models.py` - add training fields to User dataclass
2. Create `services/training_service.py` - implement pagination, formatting, keyboard creation
3. Create `services/training_view_renderer.py` - implement two-message UI rendering
4. Create `handlers/training.py` - implement /training command and 5 callback handlers
5. Update `bot.py` - register router and add command to menu
6. Update `handlers/__init__.py` - export training handler

## Key Technical Details

- Use 8 phrases per page (22 cards = 3 pages: 8, 8, 6)
- Two fixed messages: list and card
- List message: always `edit_message_text`, never deleted
- Card message: first time `send_audio` or `send_message`, then always `edit_message_media` or `edit_message_text`
- NO media_group usage (Telegram limitation)
- Single audio player with switch button
- Store message IDs in user model (persisted in users.json)
- Use audio_service to get InputMediaAudio for teacher/actor
- Callback format: `tr:action:params` for reliable parsing
- Navigation buttons check page boundaries (page 1: ignore prev, page 3: ignore next)

## Edge Cases

- Page 1: "⬅ Назад" button does nothing (check in callback)
- Page 3 (last): "➡ Вперёд" button does nothing (check in callback)
- User selects same phrase twice: just re-render card (idempotent)
- User closes card, then navigates pages: list updates normally, card_message_id is None
- User runs /training twice: reuse list_message_id (edit existing), clear card_message_id
- List message deleted by user: catch TelegramBadRequest, send new list, update list_message_id
- Card message deleted by user: catch TelegramBadRequest, send new card, update card_message_id
- Both audios missing: show text placeholder, no switch button
- One audio missing: show text placeholder when switched to missing audio, switch button still present

### To-dos

- [ ] Add TrainingSession dataclass to storage/models.py
- [ ] Create services/training_service.py with pagination and formatting logic
- [ ] Create services/training_view_renderer.py for UI rendering
- [ ] Create handlers/training.py with /training command and callbacks
- [ ] Update bot.py to register training router and add command to menu
- [ ] Update handlers/__init__.py to export training handler