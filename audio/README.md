# 🎧 Аудио файлы для FilevskiyBot

## 📂 Структура директорий

```
audio/
├── teacher/           # Голос преподавателя
│   ├── 1_myvoiceEarn.mp3
│   ├── 2_myvoiceEarn.mp3
│   └── ...
└── actor/             # Голос актера
    ├── 1_Earnest.mp3
    ├── 2_Earnest.mp3
    └── ...
```

---

## 📋 Список файлов (21 фраза)

### Голос преподавателя (teacher/):
```
1_myvoiceEarn.mp3
2_myvoiceEarn.mp3
3_myvoiceEarn.mp3
4_myvoiceEarn.mp3
5_myvoiceEarn.mp3
6_myvoiceEarn.mp3
7_myvoiceEarn.mp3
8_myvoiceEarn.mp3
9_myvoiceEarn.mp3
10_myvoiceEarn.mp3
11_myvoiceEarn.mp3
12_myvoiceEarn.mp3
13_myvoiceEarn.mp3
14_myvoiceEarn.mp3
15_myvoiceEarn.mp3
16_myvoiceEarn.mp3
17_myvoiceEarn.mp3
18_myvoiceEarn.mp3
19_myvoiceEarn.mp3
20_myvoiceEarn.mp3
21_myvoiceEarn.mp3
```

### Голос актера (actor/):
```
1_Earnest.mp3
2_Earnest.mp3
3_Earnest.mp3
4_Earnest.mp3
5_Earnest.mp3
6_Earnest.mp3
7_Earnest.mp3
8_Earnest.mp3
9_Earnest.mp3
10_Earnest.mp3
11_Earnest.mp3
12_Earnest.mp3
13_Earnest.mp3
14_Earnest.mp3
15_Earnest.mp3
16_Earnest.mp3
17_Earnest.mp3
18_Earnest.mp3
19_Earnest.mp3
20_Earnest.mp3
21_Earnest.mp3
```

---

## 📥 Как добавить файлы

### Через WSL:
```bash
cd ~/projects/FilevskiyBot

# Скопируйте ваши файлы
cp /path/to/teacher/files/*.mp3 audio/teacher/
cp /path/to/actor/files/*.mp3 audio/actor/

# Проверьте
ls audio/teacher/ | wc -l  # Должно быть 21
ls audio/actor/ | wc -l    # Должно быть 21
```

### Через Windows Explorer:
1. Откройте `\\wsl$\Ubuntu\home\tomcat\projects\FilevskiyBot\audio\teacher\`
2. Скопируйте туда файлы 1_myvoiceEarn.mp3 ... 21_myvoiceEarn.mp3
3. Откройте `\\wsl$\Ubuntu\home\tomcat\projects\FilevskiyBot\audio\actor\`
4. Скопируйте туда файлы 1_Earnest.mp3 ... 21_Earnest.mp3

---

## ✅ Требования к файлам

- **Формат**: MP3
- **Именование**: строго по шаблону `{id}_filename.mp3`
- **ID**: от 1 до 21 (совпадает с ID карточки)
- **Качество**: любое (рекомендуется 128-192 kbps)

---

## 🔍 Проверка

После добавления файлов:

```bash
cd ~/projects/FilevskiyBot

# Проверить количество
ls audio/teacher/*.mp3 | wc -l
ls audio/actor/*.mp3 | wc -l

# Проверить имена
ls audio/teacher/ | head -5
ls audio/actor/ | head -5
```

Должно быть по 21 файлу в каждой директории.

---

## 🎧 Как работает

### Без файлов (текущее состояние):
- Кнопки аудио показываются
- При нажатии: "🎧 Аудио будет добавлено позже"
- Обучение работает полностью

### С файлами:
- Первое воспроизведение: загружается из файла
- Telegram возвращает file_id
- File_id сохраняется в JSON
- Повторные воспроизведения: через file_id (быстрее!)

---

## 🚀 После добавления файлов

**НЕ нужно перезапускать бота!**

Просто:
1. Скопируйте файлы в директории
2. Отправьте `/start` боту
3. Аудио заработает автоматически!

---

## 📝 Соответствие фраз

| ID | Английская фраза | Файлы |
|----|------------------|-------|
| 1 | Charming day it has been | 1_myvoiceEarn.mp3, 1_Earnest.mp3 |
| 2 | Pray don't talk to me... | 2_myvoiceEarn.mp3, 2_Earnest.mp3 |
| ... | ... | ... |
| 21 | My own Ernest! | 21_myvoiceEarn.mp3, 21_Earnest.mp3 |

Полный список фраз смотрите в `config.py` (DEFAULT_PHRASES)

---

**Готово к использованию даже без аудио!**

Добавите файлы когда будут готовы - всё заработает автоматически! 🎵

