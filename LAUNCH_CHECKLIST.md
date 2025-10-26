# 🚀 Чеклист запуска FilevskiyBot

## ✅ Предварительная проверка

Перед запуском убедитесь:

- [x] Все файлы созданы (24 файла)
- [x] Python модули (15 .py файлов)
- [x] Скрипты исполняемые (run.sh, stop.sh)
- [x] .env файл настроен
- [x] Docker и Docker Compose установлены
- [x] Интернет соединение активно

## 📋 Шаги запуска

### 1. Проверка окружения

```bash
cd ~/projects/FilevskiyBot

# Проверить Docker
docker --version
docker-compose --version

# Проверить файлы
ls -la
```

### 2. Проверка конфигурации

```bash
# Убедиться что BOT_TOKEN корректный
cat .env

# Должно быть:
# BOT_TOKEN=8225013097:AAFr4CJZUEFIcvhKRBm9dD0dEzfm0328wPk
# TIMEZONE=Europe/Moscow
# DATA_DIR=data
# CHECK_INTERVAL=300
```

### 3. Запуск бота

```bash
./run.sh
```

Или вручную:
```bash
docker-compose up -d
```

### 4. Проверка статуса

```bash
docker-compose ps
```

Должно быть:
```
NAME                   STATUS
filevskiy_bot          Up
filevskiy_scheduler    Up
```

### 5. Просмотр логов

```bash
# Все логи
docker-compose logs -f

# Или по отдельности
docker-compose logs -f bot
docker-compose logs -f scheduler
```

Ожидаемые сообщения:
- Bot: "Bot starting..."
- Scheduler: "Scheduler started. Checking every 300 seconds..."

### 6. Тестирование в Telegram

1. Открыть Telegram
2. Найти бота: **@FilevskiyBot**
3. Отправить `/start`
4. Должно появиться приветствие и первая карточка

## 🧪 Тестовый сценарий

### Сценарий 1: Новый пользователь (обучение)

1. ✅ `/start` → приветственное сообщение
2. ✅ Карточка 1/34 с текстом "Charming day it has been,"
3. ✅ Три кнопки: ✅ Знал, 🤔 Сомневался, ❌ Не знал
4. ✅ Нажать любую кнопку → карточка 2/34
5. ✅ Пройти все 34 карточки
6. ✅ Сообщение "Поздравляю! Обучение завершено!"

### Сценарий 2: Повторение (после обучения)

1. ✅ Подождать N часов (или изменить time в data/users.json для теста)
2. ✅ Получить уведомление "У вас есть N карточек для повторения"
3. ✅ Нажать "Начать повторение"
4. ✅ Оценить карточки
5. ✅ Интервалы пересчитываются

### Сценарий 3: Проверка ANKI алгоритма

1. ✅ Нажать "❌ Не знал" → карточка вернется через 1 час
2. ✅ Нажать "🤔 Сомневался" → карточка через тот же интервал
3. ✅ Нажать "✅ Знал" → карточка через следующий интервал

## 🔍 Проверка компонентов

### Проверка хранилища

```bash
# Проверить что data/ создана
ls -la data/

# После /start должен появиться users.json
cat data/users.json | jq .
```

### Проверка логов бота

```bash
docker-compose logs bot | grep -i error
docker-compose logs bot | grep -i "Bot starting"
```

### Проверка логов scheduler

```bash
docker-compose logs scheduler | grep -i "Scheduler started"
docker-compose logs scheduler | grep -i "Checking"
```

## 🐛 Troubleshooting

### Проблема: Контейнеры не запускаются

```bash
# Проверить логи
docker-compose logs

# Пересобрать
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Проблема: Бот не отвечает

```bash
# Проверить что бот запущен
docker-compose ps

# Проверить логи на ошибки
docker-compose logs bot | tail -50

# Проверить BOT_TOKEN
cat .env | grep BOT_TOKEN
```

### Проблема: Scheduler не отправляет уведомления

```bash
# Проверить логи scheduler
docker-compose logs scheduler | tail -50

# Убедиться что есть пользователи с готовыми карточками
cat data/users.json | jq '.users | to_entries | .[0].value.cards[] | select(.status=="review")'
```

### Проблема: Данные не сохраняются

```bash
# Проверить права
ls -la data/

# Проверить volume mapping
docker-compose config | grep volumes -A 2

# Проверить что файл создается
docker-compose exec bot ls -la /app/data/
```

## 📊 Метрики успешного запуска

- [ ] Оба контейнера в статусе "Up"
- [ ] Нет ошибок в логах
- [ ] data/users.json создается после /start
- [ ] Бот отвечает на /start
- [ ] Карточки показываются с кнопками
- [ ] Прогресс отображается (N/34)
- [ ] После обучения показывается поздравление
- [ ] Scheduler пишет в лог каждые 5 минут

## 🎉 Критерии готовности к продакшену

- [ ] Бот работает 24+ часов без ошибок
- [ ] Scheduler отправляет напоминания
- [ ] Несколько пользователей протестировали
- [ ] Интервалы пересчитываются корректно
- [ ] Данные сохраняются и восстанавливаются
- [ ] Логи чистые (нет exceptions)
- [ ] Restart работает корректно

## 🔄 Процедура перезапуска

```bash
# Безопасный перезапуск (данные сохраняются)
./stop.sh
./run.sh

# Полный перезапуск с пересборкой
docker-compose down
docker-compose build
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

## 💾 Backup

### Создание backup

```bash
# Backup данных
tar -czf backup-$(date +%Y%m%d-%H%M%S).tar.gz data/

# Backup всего проекта
cd ..
tar -czf FilevskiyBot-backup-$(date +%Y%m%d).tar.gz FilevskiyBot/
```

### Восстановление

```bash
# Восстановить данные
tar -xzf backup-YYYYMMDD-HHMMSS.tar.gz
```

## 📞 Контакты и поддержка

- Bot Username: @FilevskiyBot
- Bot Token: 8225013097:AAFr4CJZUEFIcvhKRBm9dD0dEzfm0328wPk
- Project Path: ~/projects/FilevskiyBot

## 📚 Документация

- `README.md` - общее описание
- `QUICKSTART.md` - быстрый старт
- `DEPLOYMENT.md` - детальное развертывание
- `IMPLEMENTATION_REPORT.md` - отчет о реализации
- `LAUNCH_CHECKLIST.md` - этот файл

---

**Готово к запуску!** 🚀

Просто выполните:
```bash
cd ~/projects/FilevskiyBot
./run.sh
docker-compose logs -f
```

И откройте @FilevskiyBot в Telegram!

