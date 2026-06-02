# 🧟 Resident Evil Telegram Bot

> Resident Evil o'yin va kino seriyasi haqida to'liq ma'lumot beruvchi Telegram bot

## 📌 Bot haqida

Bu bot **Resident Evil** franshizasiga bag'ishlangan bo'lib, foydalanuvchilarga quyidagi imkoniyatlarni taqdim etadi:

- 🦸 RE qahramonlari haqida batafsil ma'lumot va rasmlar
- 🦹 RE yovuzlari tarixi va xususiyatlari
- 🎬 Video kliplar va sahnalar
- 📖 O'yin seriyasi tarixi
- 💰 Moliyaviy ma'lumotlar va budjet
- 🎮 O'yinlar va kinolar bo'limlari
- 🔍 Wikipedia orqali avtomatik qidiruv

## 🛠 Texnologiyalar

| Texnologiya | Versiya | Maqsad |
|-------------|---------|--------|
| Python | 3.10+ | Asosiy til |
| aiogram | 3.7.0 | Telegram Bot Framework |
| wikipedia | 1.4.0 | Avtomatik qidiruv |
| python-dotenv | 1.0.0 | Xavfsiz token saqlash |

## 📂 Loyiha tuzilmasi

```
resident-evil-bot/
├── bot.py              # Asosiy bot kodi
├── requirements.txt    # Kutubxonalar ro'yxati
├── Procfile            # Railway deploy uchun
├── .env.example        # Token namunasi
├── .gitignore          # Git uchun istisnolar
└── README.md           # Hujjat
```

## 🚀 Ishga tushirish

### 1. Repozitoriyani klonlash
```bash
git clone https://github.com/hojiakbaroktamov89-cpu/resident-evil-bot.git
cd resident-evil-bot
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Token sozlash
`.env.example` faylidan `.env` fayl yarating:
```bash
cp .env.example .env
```
`.env` faylini oching va tokeningizni kiriting:
```
BOT_TOKEN=your_telegram_bot_token
```

### 4. Botni ishga tushirish
```bash
python bot.py
```

## ☁️ Deploy (Railway)

Bot **Railway.app** platformasida doimiy ishlaydi:

1. [railway.app](https://railway.app) ga kiring
2. GitHub repo ulang
3. `BOT_TOKEN` environment variable qo'shing
4. Deploy bosing — tayyor!

## 🤖 Bot funksiyalari

### Asosiy menyu
- `🎮 Resident evilga kirish` — RE bo'limiga o'tish

### RE bo'limi
- `📖 Resident evil tarixi` — Seriya tarixi
- `🕹 Resident evil o'yinlari` — O'yinlar xronologiyasi
- `🦸‍♂️ Resident evil qahramonlari` — Leon, Ada, Chris, Ethan va boshqalar
- `🦹‍♂️ Resident evil yovuzlari` — Wesker, Nemesis, Miranda va boshqalar
- `💰 Resident evil budjeti` — Moliyaviy faktlar
- `🎬 Videolar bo'limi` — Video kliplar

### Qo'shimcha bo'limlar
- `🎮 Game interesting` — Mashhur o'yinlar (RDR2, Detroit, Cyberpunk, Genshin)
- `🎬 Movie interesting` — Mashhur seriallar (Invincible, The Boys, Supernatural, Loki)
- `✨ Favorite character` — Turli o'yin va animelerdan sevimli qahramonlar

## 👨‍💻 Muallif

**Hojiakbar Oktamov**  
GitHub: [@hojiakbaroktamov89-cpu](https://github.com/hojiakbaroktamov89-cpu)  
Telegram: [@NOOB_comeback](https://t.me/NOOB_comeback)

---
*Bu loyiha Python va aiogram 3.x frameworki yordamida yaratilgan*
