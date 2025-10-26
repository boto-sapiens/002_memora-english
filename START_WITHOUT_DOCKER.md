# 🚀 Запуск FilevskiyBot без Docker

## ✅ Успешно запущено!

Бот и scheduler работают локально через Python.

## 📊 Текущий статус

```bash
./status.sh
```

## 🔧 Управление

### Проверка статуса
```bash
pgrep -f "python bot.py" && echo "✅ Bot running" || echo "❌ Bot stopped"
pgrep -f "python scheduler_runner.py" && echo "✅ Scheduler running" || echo "❌ Scheduler stopped"
```

### Остановка
```bash
pkill -f "python bot.py"
pkill -f "python scheduler_runner.py"
```

### Запуск
```bash
cd ~/projects/FilevskiyBot
source venv/bin/activate

# Bot в фоне
nohup python bot.py > logs/bot.log 2>&1 &

# Scheduler в фоне  
nohup python scheduler_runner.py > logs/scheduler.log 2>&1 &
```

## 📱 Тестирование

1. Откройте Telegram
2. Найдите: **@FilevskiyBot**
3. Отправьте: `/start`
4. Вы должны увидеть приветствие и первую карточку!

## 📝 Просмотр логов

```bash
# Логи бота
tail -f logs/bot.log

# Логи scheduler
tail -f logs/scheduler.log

# Данные пользователей
cat data/users.json
```

## 🐛 Отладка

Если бот не отвечает:

1. Проверьте что процессы запущены:
   ```bash
   ps aux | grep python
   ```

2. Проверьте логи на ошибки:
   ```bash
   grep -i error logs/bot.log
   ```

3. Проверьте BOT_TOKEN:
   ```bash
   cat .env | grep BOT_TOKEN
   ```

4. Перезапустите:
   ```bash
   pkill -f python
   source venv/bin/activate
   python bot.py &
   python scheduler_runner.py &
   ```

## ✅ Бот работает если:

- Процессы bot.py и scheduler_runner.py запущены
- Нет ошибок в логах
- data/users.json создается после /start
- Бот отвечает в Telegram

## 🎉 Готово!

Теперь просто отправьте `/start` боту @FilevskiyBot в Telegram!

