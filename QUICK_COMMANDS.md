# 🚀 Быстрые команды для FilevskiyBot

## Управление ботом

### Запуск
```bash
cd ~/projects/FilevskiyBot
source venv/bin/activate
nohup python bot.py > logs/bot.log 2>&1 &
nohup python scheduler_runner.py > logs/scheduler.log 2>&1 &
```

### Проверка статуса
```bash
pgrep -f "python bot.py" && echo "✅ Bot running" || echo "❌ Bot stopped"
pgrep -f "python scheduler" && echo "✅ Scheduler running" || echo "❌ Scheduler stopped"
```

### Остановка
```bash
pkill -f "python bot.py"
pkill -f "python scheduler_runner.py"
```

### Просмотр логов
```bash
tail -f ~/projects/FilevskiyBot/logs/bot.log
tail -f ~/projects/FilevskiyBot/logs/scheduler.log
```

### Полный перезапуск
```bash
cd ~/projects/FilevskiyBot
pkill -f "python.*bot"
pkill -f "python.*scheduler"
sleep 2
source venv/bin/activate
nohup python bot.py > logs/bot.log 2>&1 &
nohup python scheduler_runner.py > logs/scheduler.log 2>&1 &
```

## Отладка

### Проверить фразы
```bash
cd ~/projects/FilevskiyBot
source venv/bin/activate
python check_phrases.py
```

### Проверить статус пользователя
```bash
cd ~/projects/FilevskiyBot
source venv/bin/activate
python check_user_status.py
```

### Отправить тестовое сообщение
```bash
cd ~/projects/FilevskiyBot
source venv/bin/activate
python test_message.py
```

### Очистить данные пользователей (осторожно!)
```bash
cd ~/projects/FilevskiyBot
rm data/users.json
# Теперь все пользователи будут новыми при /start
```

## Данные

### Просмотр пользователей
```bash
cat ~/projects/FilevskiyBot/data/users.json | head -50
```

### Количество пользователей
```bash
cat ~/projects/FilevskiyBot/data/users.json | grep -o '"telegram_id":' | wc -l
```

## Полезные файлы

- `config.py` - настройки и фразы
- `data/users.json` - данные пользователей
- `logs/bot.log` - логи бота
- `logs/scheduler.log` - логи scheduler

---

**Текущий статус**: Бот работает! 🎉
- Фразы: 21 словосочетание
- Telegram: @FilevskiyBot
- Команда: /start

