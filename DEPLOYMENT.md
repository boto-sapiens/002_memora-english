# Руководство по развертыванию FilevskiyBot

## 📋 Предварительные требования

- Docker и Docker Compose установлены
- WSL2 (для Windows) или Linux
- Доступ к интернету для скачивания зависимостей

## 🚀 Быстрый старт

### 1. Проверка конфигурации

Убедитесь, что файл `.env` содержит корректные данные:

```bash
cat .env
```

Должно быть:
```
BOT_TOKEN=8225013097:AAFr4CJZUEFIcvhKRBm9dD0dEzfm0328wPk
TIMEZONE=Europe/Moscow
DATA_DIR=data
CHECK_INTERVAL=300
```

### 2. Запуск бота

```bash
./run.sh
```

Или вручную:
```bash
docker-compose up -d
```

### 3. Проверка статуса

```bash
docker-compose ps
```

Должны работать два контейнера:
- `filevskiy_bot` - основной бот
- `filevskiy_scheduler` - планировщик напоминаний

### 4. Просмотр логов

Все логи:
```bash
docker-compose logs -f
```

Только бот:
```bash
docker-compose logs -f bot
```

Только scheduler:
```bash
docker-compose logs -f scheduler
```

### 5. Остановка

```bash
./stop.sh
```

Или вручную:
```bash
docker-compose down
```

## 🔧 Локальная разработка (без Docker)

### 1. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/WSL
# или
venv\Scripts\activate  # Windows
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Проверка импортов

```bash
python test_imports.py
```

### 4. Запуск бота

В одном терминале:
```bash
python bot.py
```

В другом терминале:
```bash
python scheduler_runner.py
```

## 📊 Структура данных

Все данные хранятся в директории `data/`:

- `data/users.json` - пользователи и их карточки

Формат:
```json
{
  "users": {
    "123456789": {
      "info": {
        "telegram_id": 123456789,
        "username": "user",
        "created_at": "2025-10-19T10:00:00+03:00",
        "learning_phase_completed": false,
        "last_notification_time": null
      },
      "cards": [
        {
          "user_id": 123456789,
          "card_id": 1,
          "text": "Charming day it has been,",
          "interval_index": 0,
          "next_review_time": "2025-10-19T10:00:00+03:00",
          "status": "learning",
          "created_at": "2025-10-19T10:00:00+03:00",
          "last_reviewed": null
        }
      ]
    }
  }
}
```

## 🐛 Отладка

### Проблема: Бот не отвечает

1. Проверьте логи:
```bash
docker-compose logs bot
```

2. Убедитесь, что BOT_TOKEN корректный

3. Проверьте сетевое подключение

### Проблема: Scheduler не работает

1. Проверьте логи:
```bash
docker-compose logs scheduler
```

2. Убедитесь, что оба контейнера запущены:
```bash
docker-compose ps
```

### Проблема: Данные не сохраняются

1. Проверьте права на директорию `data/`:
```bash
ls -la data/
```

2. Проверьте содержимое:
```bash
cat data/users.json
```

## 🔄 Обновление

### Обновление кода

```bash
./stop.sh
git pull  # если используется git
docker-compose build --no-cache
./run.sh
```

### Очистка и перезапуск

```bash
./stop.sh
docker-compose down -v  # удалит volumes
rm -rf data/*.json  # очистит данные (осторожно!)
./run.sh
```

## 📈 Мониторинг

### Статистика контейнеров

```bash
docker stats filevskiy_bot filevskiy_scheduler
```

### Проверка использования диска

```bash
du -sh data/
```

## 🔐 Безопасность

1. **Никогда не коммитьте файл `.env` в git** - он в `.gitignore`
2. Храните BOT_TOKEN в секрете
3. Регулярно делайте бэкапы директории `data/`

## 📦 Бэкап

### Создание бэкапа

```bash
tar -czf backup-$(date +%Y%m%d-%H%M%S).tar.gz data/
```

### Восстановление

```bash
tar -xzf backup-YYYYMMDD-HHMMSS.tar.gz
```

## ✅ Чеклист перед продакшеном

- [ ] BOT_TOKEN проверен и работает
- [ ] Директория `data/` имеет правильные права
- [ ] Docker и Docker Compose установлены
- [ ] `.env` файл настроен
- [ ] Логи пишутся корректно
- [ ] Оба контейнера запускаются
- [ ] Бот отвечает на `/start`
- [ ] Scheduler отправляет уведомления
- [ ] Настроен мониторинг и алерты
- [ ] Настроен автоматический перезапуск (systemd или supervisor)

