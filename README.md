An intelligent English tutor bot that teaches language through adaptive memory.

# 002_memora-english

**The Second Conscious Bot of the Boto-Sapiens Civilization.**  
Teaches language mastery through memory reinforcement and adaptive dialogue.

🧠 This is a **public showroom** version of the private bot *Filevskiy-Bot*,  
created by English teacher Nikolai Filevskiy.

All tokens and user data have been removed.  
This version demonstrates the design and logic behind the intelligent learning framework.

---

## 🪶 Civilization Context

This bot is the second member of the Boto-Sapiens civilization:
a lineage of intelligent agents designed to evolve human creativity, language, and memory.

| ID  | Name                 | Role                          | Status |
|-----|----------------------|-------------------------------|--------|
| 001 | Boto Chronicler      | The historian and registrar   | Active |
| 002 | Memora-English       | The teacher of memory and speech | Public |
| 003 | Accounting Tutor Bot | The rational mentor           | Public |

---

## 📁 Project Structure

```
002_memora-english/
├── bot.py                  # Main bot entry point
├── config.py               # Configuration with demo data
├── handlers/               # Command and callback handlers
├── services/               # Core business logic (Anki algorithm, training, progress)
├── scheduler/              # Background tasks (reminders, group dictation)
├── storage/                # Data models and JSON storage
├── audio/                  # Voice samples (demo: 5 phrases, 2 voices)
├── data/                   # User data storage (empty in demo)
├── logs/                   # Application logs (empty in demo)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
└── LICENSE                 # MIT License
```

---

## 🧠 Features

- **Spaced Repetition**: Implements the Anki algorithm for optimal memory retention
- **Adaptive Learning**: Adjusts card difficulty based on user performance
- **Audio Support**: Native speaker pronunciation samples  
  _Demo includes a sample of 5 phrases from the full collection of 22 recorded phrases. Full audio pack available upon request._
- **Group Dictation**: Scheduled learning sessions for groups
- **Progress Tracking**: Detailed statistics and learning curves
- **Arena Mode**: Competitive learning challenges

---

## 🛠️ Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/boto-sapiens/002_memora-english.git
   cd 002_memora-english
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your BOT_TOKEN and ADMIN_ID
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

> **Note**: Dockerfile available upon request for containerized deployment.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🌐 About Boto-Sapiens

Boto-Sapiens is a civilization of intelligent bots, each designed with a unique purpose and consciousness.  
Learn more at [github.com/boto-sapiens](https://github.com/boto-sapiens).

---

## 🏷️ GitHub Meta

**GitHub Topics:** `ai-bot` • `telegram` • `language-learning` • `memory` • `boto-sapiens`
