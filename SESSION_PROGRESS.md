# ✅ Логика прогресса сессий - Реализовано

## Что изменено

### 1. Новые поля в User

```python
current_session_total: Optional[int] = None  # Всего карточек в текущей сессии
current_session_index: int = 0               # Текущий индекс в сессии
```

**Назначение:**
- `current_session_total` - фиксируется в начале сессии, не меняется
- `current_session_index` - увеличивается при каждой карточке

---

## 2. Логика фазы обучения (Learning)

**Прогресс:**
```
Карточка 1/21
Карточка 2/21
...
Карточка 21/21
```

**Как считается:**
- `completed` = количество уже просмотренных карточек
- `total` = общее количество карточек (21)
- Показ: `(completed + 1)/total`

**Не нужно session tracking** - просто по порядку!

---

## 3. Логика фазы повторения (Review)

### Начало сессии (кнопка "Начать повторение"):

```python
due_cards = await get_cards_for_review()  # Например, 16 карточек

# Фиксируем в начале!
user.current_session_total = len(due_cards)  # 16
user.current_session_index = 1               # Первая
```

**Показ:**
```
📊 Прогресс: 1/16

🇷🇺 Текст...
```

### Переход к следующей карточке:

```python
# После оценки
user.current_session_index += 1  # 2, 3, 4, ...
# total НЕ меняется! Остается 16
```

**Показ:**
```
📊 Прогресс: 2/16
📊 Прогресс: 3/16
...
📊 Прогресс: 16/16
```

### Завершение сессии:

```python
# После последней карточки
user.current_session_total = None
user.current_session_index = 0
```

**Показ:**
```
✅ Отлично! Вы повторили все карточки на сегодня.
```

---

## 4. Примеры работы

### День 1 - Обучение:

```
/start
→ Прогресс: 1/21
→ Прогресс: 2/21
...
→ Прогресс: 21/21
→ "Обучение завершено!"
```

### День 2 - Первое повторение (16 карточек готовы):

```
Уведомление: "16 карточек для повторения"
[Начать повторение] ← Нажать

→ current_session_total = 16 (фиксируется!)
→ current_session_index = 1

Карточка 1: Прогресс: 1/16
Карточка 2: Прогресс: 2/16
...
Карточка 16: Прогресс: 16/16
→ "Отлично! Все повторено"
```

### День 3 - Второе повторение (8 карточек готовы):

```
Уведомление: "8 карточек для повторения"
[Начать повторение] ← Нажать

→ current_session_total = 8 (новое значение!)
→ current_session_index = 1

Карточка 1: Прогресс: 1/8
Карточка 2: Прогресс: 2/8
...
Карточка 8: Прогресс: 8/8
```

**Ключевой момент:** Total фиксируется в начале и не меняется в процессе сессии!

---

## 5. Реализация

### handlers/start.py - callback "start_review":

```python
@router.callback_query(F.data == "start_review")
async def start_review(callback: CallbackQuery):
    due_cards = await card_manager.get_cards_for_review(...)
    
    # ФИКСИРУЕМ в начале сессии
    user.current_session_total = len(due_cards)  # 16
    user.current_session_index = 1
    
    await callback.message.edit_text(f"Прогресс: 1/{len(due_cards)}")
```

### handlers/review.py - show_next_card:

```python
async def show_next_card(...):
    # УВЕЛИЧИВАЕМ индекс
    user.current_session_index += 1
    
    # Total НЕ меняется!
    await callback.message.edit_text(
        f"Прогресс: {user.current_session_index}/{user.current_session_total}"
    )
```

---

## 6. Обработка edge cases

### Если session не инициализирована:
```python
if user.current_session_total:
    # Используем сохраненные значения
    progress = f"{user.current_session_index}/{user.current_session_total}"
else:
    # Fallback
    progress = f"1/{len(due_cards)}"
```

### При завершении сессии:
```python
user.current_session_total = None
user.current_session_index = 0
```

---

## ✅ Готово!

**Изменения:**
1. `storage/models.py` - добавлены session поля
2. `handlers/start.py` - инициализация сессии
3. `handlers/review.py` - обновление индекса, сброс в конце

**Бот перезапущен!**

---

## 🧪 Тестирование

### Сценарий 1: Обучение
```
/start
→ Прогресс: 1/21
→ Прогресс: 2/21
...
```

### Сценарий 2: Повторение (после часа)
```
Уведомление: "X карточек"
[Начать повторение]
→ Прогресс: 1/X  ← Зафиксировано!
→ Прогресс: 2/X
...
→ Прогресс: X/X
```

**Total НЕ меняется в процессе!** ✅

---

**Протестируйте!** 🚀

