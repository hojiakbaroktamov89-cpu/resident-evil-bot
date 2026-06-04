<div align="center">

# 🧟 Resident Evil Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.7.0-green?style=for-the-badge)](https://aiogram.dev)
[![Railway](https://img.shields.io/badge/Deployed-Railway-purple?style=for-the-badge)](https://railway.app)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **A feature-rich Telegram bot dedicated to the entire Resident Evil universe — characters, villains, game history, videos, and more.**

[🤖 Try the Bot](https://t.me/your_bot_username) • [📢 Channel](https://t.me/just_live_1_8) • [👤 Developer](https://t.me/NOOB_comeback)

</div>

---

## 📸 Preview

```
🎮 Start the bot → Subscribe to channel → Explore RE Universe
      ↓
📖 History | 🕹 Games | 🦸 Heroes | 🦹 Villains | 💰 Budget | 🎬 Videos
      ↓
🎮 Game Interesting | 🎬 Movie Interesting | ✨ Favorite Characters
```

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🦸 **RE Heroes** | Detailed info & photos of Leon, Ada, Chris, Ethan, Jill, Claire and more |
| 🦹 **RE Villains** | Deep backstories of Wesker, Nemesis, Mother Miranda, Mr. X and others |
| 📖 **RE History** | Complete lore from Umbrella's founding to Village |
| 🕹 **RE Games** | Full chronological list from RE0 to RE8 Village |
| 🎬 **Video Section** | Exclusive video clips: History L, Requiem, Luis Sera, Hunk, RE Evolution |
| 💰 **RE Budget** | Box office stats, sales figures, and franchise financial data |
| 🎮 **Game Section** | RDR2, Detroit: Become Human, Cyberpunk 2077, Genshin Impact |
| 📺 **Movie Section** | Invincible, The Boys, Supernatural, Loki |
| ✨ **Favorite Characters** | Noob Saibot, Ghost, Batman, Light Yagami, Connor, Makima, Dante, Kratos & more |
| 🔍 **Smart Search** | Auto Wikipedia search for any unknown topic in Uzbek |
| 📢 **Channel Guard** | Users must subscribe to channel before using the bot |

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | 3.11 | Core language |
| ![aiogram](https://img.shields.io/badge/-aiogram-2CA5E0?logo=telegram&logoColor=white) | 3.7.0 | Telegram Bot Framework |
| Wikipedia API | 1.4.0 | Auto search integration |
| python-dotenv | 1.0.0 | Secure token management |
| Railway | — | 24/7 Cloud Deployment |

---

## 📂 Project Structure

```
resident-evil-bot/
│
├── 🐍 bot.py              # Main bot logic (handlers, keyboards, media)
├── 📋 requirements.txt    # Python dependencies
├── 🚂 Procfile            # Railway deployment config
├── 🐍 .python-version     # Python version pin (3.11)
├── 🔒 .env.example        # Environment variable template
├── 🚫 .gitignore          # Git ignore rules
└── 📖 README.md           # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### 1. Clone the repository
```bash
git clone https://github.com/hojiakbaroktamov89-cpu/resident-evil-bot.git
cd resident-evil-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and add your token:
```env
BOT_TOKEN=your_telegram_bot_token_here
```

### 4. Run the bot
```bash
python bot.py
```

---

## ☁️ Deployment on Railway

This bot is deployed and running **24/7** on [Railway.app](https://railway.app).

### Deploy your own instance:

1. Fork this repository
2. Go to [railway.app](https://railway.app) → **New Project**
3. Select **Deploy from GitHub repo**
4. Choose `resident-evil-bot`
5. Go to **Variables** → Add:
   ```
   BOT_TOKEN = your_token_here
   ```
6. Click **Deploy** — done! 🎉

---

## 🤖 Bot Commands & Navigation

### Main Menu
```
/start → Welcome screen (with channel subscription check)
🎮 Enter Resident Evil → Opens RE main menu
```

### RE Main Menu
```
📖 RE History          → Full lore from 1960s to present
🕹 RE Games            → RE0 through RE8 Village
🦸 RE Heroes           → All protagonist profiles
🦹 RE Villains         → All antagonist profiles
💰 RE Budget           → Financial stats & records
🎬 Video Section       → Exclusive video content
➡️ Next Section        → Game & Movie interests
```

### Heroes Available
```
Leon S. Kennedy | Ada Wong | Chris Redfield | Ethan Winters
Jill Valentine | Claire Redfield | Mia Winters | Zoe Baker
Sherry Birkin | Jake Muller | Rebecca Chambers
```

### Villains Available
```
Albert Wesker | Mr. X | Nemesis | Mother Miranda
Krauser | Ramon Salazar | Jack Baker | Eveline
```

### Extra Sections
```
🎮 Game Interesting    → RDR2 | Detroit | Cyberpunk 2077 | Genshin Impact
🎬 Movie Interesting   → Invincible | The Boys | Supernatural | Loki
✨ Favorite Characters → 10+ characters from various games & anime
```

---

## 📊 Bot Statistics

- **Total Characters:** 19 heroes + villains
- **Video Content:** 5 exclusive clips
- **Game Coverage:** 9 RE titles (RE0 → RE8)
- **Extra Content:** 4 games + 4 TV shows + 10 favorite characters
- **Language Support:** Uzbek 🇺🇿

---

## 🔐 Security

- Bot token is stored as an **environment variable** — never hardcoded
- `.env` file is excluded from Git via `.gitignore`
- Channel subscription verification before bot access

---

## 👨‍💻 Developer

<div align="center">

### Hojiakbar Oktamov

[![GitHub](https://img.shields.io/badge/GitHub-hojiakbaroktamov89--cpu-181717?style=for-the-badge&logo=github)](https://github.com/hojiakbaroktamov89-cpu)
[![Telegram](https://img.shields.io/badge/Telegram-@NOOB__comeback-2CA5E0?style=for-the-badge&logo=telegram)](https://t.me/NOOB_comeback)

*"just young creator"*

</div>

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use and modify.

---

<div align="center">

**Made with ❤️ and Python**

*If you like this project, give it a ⭐ on GitHub!*

</div>
