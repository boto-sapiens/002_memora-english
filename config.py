"""Configuration module - loads settings from environment variables"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "DEMO_TOKEN_PLACEHOLDER")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
MODE = os.getenv("MODE", "DEMO")

# Arena configuration (optional features)
ARENA_URL = os.getenv("ARENA_URL", "http://localhost:8000")
ARENA_ENABLED = os.getenv("ARENA_ENABLED", "false").lower() == "true"
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID", "0")) if os.getenv("TARGET_CHAT_ID") else None

# Scheduler configuration
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "3600"))  # Default: 1 hour

# Storage configuration
DATA_DIR = os.getenv("DATA_DIR", "./data")

# Timezone configuration
TIMEZONE = os.getenv("TIMEZONE", "Asia/Bangkok")

# Anki algorithm intervals (in seconds)
# Pattern: 1m, 10m, 1h, 4h, 1d, 3d, 1w, 2w, 1mo, 3mo, 6mo
INTERVALS = [
    60,          # 0: 1 minute
    600,         # 1: 10 minutes
    3600,        # 2: 1 hour
    14400,       # 3: 4 hours
    86400,       # 4: 1 day
    259200,      # 5: 3 days
    604800,      # 6: 1 week
    1209600,     # 7: 2 weeks
    2592000,     # 8: 1 month
    7776000,     # 9: 3 months
    15552000     # 10: 6 months
]

# Demo phrases for language learning
DEFAULT_PHRASES = [
    {"id": 1, "text_en": "To be or not to be", "text_ru": "Быть или не быть", "actor_audio": "1_Earnest.mp3", "teacher_audio": "1_myvoiceEarn.mp3"},
    {"id": 2, "text_en": "The importance of being earnest", "text_ru": "Как важно быть серьёзным", "actor_audio": "2_Earnest.mp3", "teacher_audio": "2_myvoiceEarn.mp3"},
    {"id": 3, "text_en": "A trivial comedy for serious people", "text_ru": "Несерьёзная комедия для серьёзных людей", "actor_audio": "3_Earnest.mp3", "teacher_audio": "3_myvoiceEarn.mp3"},
    {"id": 4, "text_en": "I am sick to death of cleverness", "text_ru": "Меня тошнит от этой умности", "actor_audio": "4_Earnest.mp3", "teacher_audio": "4_myvoiceEarn.mp3"},
    {"id": 5, "text_en": "All women become like their mothers", "text_ru": "Все женщины становятся похожи на своих матерей", "actor_audio": "5_Earnest.mp3", "teacher_audio": "5_myvoiceEarn.mp3"},
    {"id": 6, "text_en": "That is their tragedy", "text_ru": "В этом их трагедия", "actor_audio": "6_Earnest.mp3", "teacher_audio": "6_myvoiceEarn.mp3"},
    {"id": 7, "text_en": "No man does", "text_ru": "Ни один мужчина не похож", "actor_audio": "7_Earnest.mp3", "teacher_audio": "7_myvoiceEarn.mp3"},
    {"id": 8, "text_en": "And that is his", "text_ru": "И в этом его трагедия", "actor_audio": "8_Earnest.mp3", "teacher_audio": "8_myvoiceEarn.mp3"},
    {"id": 9, "text_en": "I hope you have not been leading a double life", "text_ru": "Надеюсь, ты не ведёшь двойную жизнь", "actor_audio": "9_Earnest.mp3", "teacher_audio": "9_myvoiceEarn.mp3"},
    {"id": 10, "text_en": "Pretending to be wicked and being good all the time", "text_ru": "Притворяешься плохим, а на самом деле всё время хороший", "actor_audio": "10_Earnest.mp3", "teacher_audio": "10_myvoiceEarn.mp3"},
    {"id": 11, "text_en": "That would be hypocrisy", "text_ru": "Это было бы лицемерием", "actor_audio": "11_Earnest.mp3", "teacher_audio": "11_myvoiceEarn.mp3"},
    {"id": 12, "text_en": "The truth is rarely pure and never simple", "text_ru": "Правда редко бывает чистой и никогда не бывает простой", "actor_audio": "12_Earnest.mp3", "teacher_audio": "12_myvoiceEarn.mp3"},
    {"id": 13, "text_en": "Modern life would be very tedious", "text_ru": "Современная жизнь была бы очень скучной", "actor_audio": "13_Earnest.mp3", "teacher_audio": "13_myvoiceEarn.mp3"},
    {"id": 14, "text_en": "If it were either", "text_ru": "Будь правда чистой или простой", "actor_audio": "14_Earnest.mp3", "teacher_audio": "14_myvoiceEarn.mp3"},
    {"id": 15, "text_en": "And modern literature a complete impossibility", "text_ru": "А современная литература была бы совершенно невозможна", "actor_audio": "15_Earnest.mp3", "teacher_audio": "15_myvoiceEarn.mp3"},
    {"id": 16, "text_en": "I never travel without my diary", "text_ru": "Я никогда не путешествую без своего дневника", "actor_audio": "16_Earnest.mp3", "teacher_audio": "16_myvoiceEarn.mp3"},
    {"id": 17, "text_en": "One should always have something sensational to read in the train", "text_ru": "В поезде всегда нужно иметь что-то сенсационное для чтения", "actor_audio": "17_Earnest.mp3", "teacher_audio": "17_myvoiceEarn.mp3"},
    {"id": 18, "text_en": "We live in an age of surfaces", "text_ru": "Мы живём в эпоху поверхностей", "actor_audio": "18_Earnest.mp3", "teacher_audio": "18_myvoiceEarn.mp3"},
    {"id": 19, "text_en": "I like persons better than principles", "text_ru": "Мне люди нравятся больше принципов", "actor_audio": "19_Earnest.mp3", "teacher_audio": "19_myvoiceEarn.mp3"},
    {"id": 20, "text_en": "And I like persons with no principles better than anything else", "text_ru": "А люди без принципов нравятся мне больше всего", "actor_audio": "20_Earnest.mp3", "teacher_audio": "20_myvoiceEarn.mp3"},
    {"id": 21, "text_en": "In matters of grave importance, style, not sincerity is the vital thing", "text_ru": "В вопросах огромной важности стиль, а не искренность - вот что главное", "actor_audio": "21_Earnest.mp3", "teacher_audio": "21_myvoiceEarn.mp3"},
    {"id": 22, "text_en": "I really don't see anything romantic in proposing", "text_ru": "Я не вижу ничего романтичного в предложении руки", "actor_audio": "22_Earnest.mp3", "teacher_audio": "22_myvoiceEarn.mp3"},
]

# Validate configuration
if BOT_TOKEN == "DEMO_TOKEN_PLACEHOLDER" or MODE == "DEMO":
    print("⚠️ Running in DEMO mode - bot will not connect to Telegram")
    print("⚠️ Please set BOT_TOKEN and MODE in .env file for production use")

