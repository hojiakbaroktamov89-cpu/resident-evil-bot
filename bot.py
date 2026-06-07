import asyncio
import logging
import sys
import os
import requests
import wikipedia
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.client.default import DefaultBotProperties

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
wikipedia.set_lang("uz")

router = Router()

@router.message(F.text == "/geminitest")
async def test_gemini(message: Message):
    await message.answer(f"KEY: {str(GEMINI_API_KEY)[:10]}...")
    result = ask_gemini("salom")
    if result:
        await message.answer(f"✅ ISHLADI: {result[:100]}")
    else:
        await message.answer("❌ ISHLAMADI - key None yoki xato")

def ask_gemini(savol: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = (
        f"Sen Resident Evil o'yini va boshqa o'yinlar haqida bilimdon yordamchisan. "
        f"Foydalanuvchi so'radi: {savol}. "
        f"O'zbek tilida qisqa javob ber."
    )
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=data, timeout=15)
        print(f"GEMINI STATUS: {r.status_code}")
        print(f"GEMINI RESPONSE: {r.text[:300]}")
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return None
    except Exception as e:
        print(f"GEMINI XATO: {e}")
        return None

main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎮 Resident evilga kirish")]],
    resize_keyboard=True
    )

sub_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Kanalga o'tish 📢", url="https://t.me/just_live_1_8")],
        [InlineKeyboardButton(text="Obunani tekshirish ✅", callback_data="check_subscription")],
        [InlineKeyboardButton(text="Ulashish 🚀", switch_inline_query="Resident Evil haqida hamma narsani shu botdan topasiz! 🧟")]
    ]
)

CHANNELS = ["@just_live_1_8"]

async def check_sub(bot: Bot, user_id: int):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["member", "administrator", "creator"]:
                return True
        except Exception as e:
            print(f"Xatolik: {e}")
            return False
    return False

@router.message(F.video)
async def get_video_id(message: Message):
    video_id = message.video.file_id
    await message.reply(
        f"✅ <b>Video qabul qilindi!</b>\n\n"
        f"🆔 <b>file_id:</b>\n<code>{video_id}</code>",
        parse_mode="HTML"
    )

@router.message(F.video_note)
async def get_video_note_id(message: Message):
    video_note_id = message.video_note.file_id
    await message.reply(f"📹 **Video xabar ID:**\n`{video_note_id}`", parse_mode="Markdown")

re_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Resident evil tarixi"), KeyboardButton(text="🕹 Resident evil o'yinlari")],
        [KeyboardButton(text="🦸‍♂️ Resident evil qahramonlari"), KeyboardButton(text="🦹‍♂️ Resident evil yovuzlari")],
        [KeyboardButton(text="💰 Resident evil budjeti"), KeyboardButton(text="🎬 Videolar bo'limi")],
        [KeyboardButton(text="➡️ Keyingi bo'limga o'tish"), KeyboardButton(text="⬅️ Ortga")]
    ],
    resize_keyboard=True
)

re_main_kb1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 Game interesting"), KeyboardButton(text="🎬 Movie intersting")],
        [KeyboardButton(text="✨ Favorite character"), KeyboardButton(text="⬅️ Ortga menyuga")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "➡️ Keyingi bo'limga o'tish")
async def go_to_next_section(message: Message):
    await message.answer(
        "Siz keyingi bo'limga o'tdingiz. Quyidagilardan birini tanlang 👇",
        reply_markup=re_main_kb1
    )

@router.message(F.text == "⬅️ Ortga menyuga")
async def go_back(message: Message):
    await message.answer(
        "Asosiy menyuga qaytdingiz 👇",
        reply_markup=re_main_kb
    )

character_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🥷 Noob Saibot"), KeyboardButton(text="💀 Ghost")],
        [KeyboardButton(text="🦇 Batman"), KeyboardButton(text="📓 Light Yagami")],
        [KeyboardButton(text="🤖 Connor"),KeyboardButton(text="Keyingi sahifa ➡️")],
        [KeyboardButton(text="⬅️ Orqaga (Kino/O'yin bo'limiga)")]
    ],
    resize_keyboard=True
)

character_kb2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👁 Makima 👁"), KeyboardButton(text="🔴 Dante")],
        [KeyboardButton(text="❌ Arlecchino ❌"), KeyboardButton(text="🪓 Kratos")],
        [KeyboardButton(text="⬅️ Oldingi sahifa"), KeyboardButton(text="⬅️ Orqaga (Kino/O'yin bo'limiga)")]
    ],
    resize_keyboard=True
)

game_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🤠 Red Dead Redemption 2"), KeyboardButton(text="🤖 Detroit: Become Human")],
        [KeyboardButton(text="🌆 Cyberpunk 2077"), KeyboardButton(text="✨ Genshin Impact")],
        [KeyboardButton(text="⬅️ Orqaga (Kino/O'yin bo'limiga)")]
    ],
    resize_keyboard=True
)

movie_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🩸 Invincible"), KeyboardButton(text="🦸‍♂️ The Boys")],
        [KeyboardButton(text="👻 Supernatural"), KeyboardButton(text="⏳ Loki")],
        [KeyboardButton(text="⬅️ Orqaga (Kino/O'yin bo'limiga)")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "🎬 Movie intersting")
async def show_movie_interesting(message: Message):
    await message.answer(
        "🎬 <b>Kino va Seriallar olamiga xush kelibsiz!</b>\n\n"
        "Quyidagi mashhur seriallardan birini tanlang 👇",
        reply_markup=movie_kb,
        parse_mode="HTML"
    )

@router.message(F.text == "🎮 Game interesting")
async def show_game_interesting(message: Message):
    try:
        await message.answer(
            "🎮 <b>O'yinlar olamiga xush kelibsiz!</b>\n\n"
            "Quyidagi o'yinlardan birini tanlang:",
            reply_markup=game_kb,
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"Xatolik: {e}")

@router.message(F.text == "⬅️ Orqaga (Kino/O'yin bo'limiga)")
async def go_back_to_main1(message: Message):
    await message.answer(
        "Kino va O'yinlar bo'limi 👇",
        reply_markup=re_main_kb1
    )

heroes_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Leon S. Kennedy"), KeyboardButton(text="Ada Wong")],
        [KeyboardButton(text="Chris Redfield"), KeyboardButton(text="Ethan Winters")],
        [KeyboardButton(text="Jill Valentine"), KeyboardButton(text="Claire Redfield")],
        [KeyboardButton(text="Keyingi qahramonlar ➡️"),KeyboardButton(text="⬅️ RE Menyuga qaytish")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "⬅️ Oldingi qahramonlar")
async def back_to_heroes_p1(message: Message):
    await message.answer("Qahramonlar (1-qism):", reply_markup=heroes_kb)

heroes_kb2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Mia Winters"), KeyboardButton(text="Zoe Baker")],
        [KeyboardButton(text="Sherry Birkin"), KeyboardButton(text="Jake Muller")],
        [KeyboardButton(text="Rebecca Chambers")],
        [KeyboardButton(text="⬅️ Oldingi qahramonlar"),KeyboardButton(text="⬅️ RE Menyuga qaytish")]
    ]
)

villains_kb1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Albert Wesker"), KeyboardButton(text="Mr. X")],
        [KeyboardButton(text="Nemesis"), KeyboardButton(text="Mother Miranda")],
        [KeyboardButton(text="Keyingi yovuzlar ➡️")],
        [KeyboardButton(text="⬅️ RE Menyuga qaytish")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "⬅️ Oldingi yovuzlar")
async def back_to_villains_p1(message: Message):
    await message.answer("Yovuzlar (1-qism):", reply_markup=villains_kb1)

villains_kb2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=" Krauser"), KeyboardButton(text="Ramon Salazar")],
        [KeyboardButton(text="Jack Baker"), KeyboardButton(text="Eveline")],
        [KeyboardButton(text="⬅️ Oldingi yovuzlar")],
        [KeyboardButton(text="⬅️ RE Menyuga qaytish")]
    ],
    resize_keyboard=True
)

video_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎬 History L"), KeyboardButton(text="🧾 Requiem")],
        [KeyboardButton(text="🔬 Luis Sera"), KeyboardButton(text="💀 Hunk")],
        [KeyboardButton(text="🎮 RE Evolution (1996-2026)"), KeyboardButton(text="⬅️ RE Menyuga qaytish")]
    ],
    resize_keyboard=True
)

@router.message(CommandStart())
async def start_cmd(message: Message, bot: Bot):
    user_sub = await check_sub(bot, message.from_user.id)
    if user_sub:
        await message.answer("Xush kelibsiz! Botdan foydalanishingiz mumkin.", reply_markup=main_kb)
    else:
        await message.answer("Botdan foydalanish uchun kanalga obuna bo'ling!", reply_markup=sub_kb)

@router.message(F.text == "✨ Favorite character")
async def show_favorite_characters(message: Message):
    await message.answer(
        "✨ <b>Sizning sevimli qahramonlaringiz bo'limi!</b>\n\n"
        "Qaysi qahramon haqida video va ma'lumot ko'rmoqchisiz? Tanlang 👇",
        reply_markup=character_kb,
        parse_mode="HTML"
    )

@router.message(F.text == "Keyingi sahifa ➡️")
async def show_favorite_characters_page2(message: Message):
    await message.answer(
        "✨ <b>Sizning sevimli qahramonlaringiz — 2-sahifa</b>\n\n"
        "Yangi qahramonlarni tanlang 👇",
        reply_markup=character_kb2,
        parse_mode="HTML"
    )

@router.message(F.text == "⬅️ Oldingi sahifa")
async def go_back_to_page1(message: Message):
    await message.answer(
        "1-sahifaga qaytdingiz 👇",
        reply_markup=character_kb
    )

@router.message(F.text == "🪓 Kratos")
async def kratos_info(message: Message):
    media_id = "BAACAgIAAxkBAAIB2moX_zNlAAGxyuEXNcifCRHuRPXoggACapgAArV9wUiZ22M3howNuDsE"
    caption_text = "<b>🪓 Kratos (Sparta Sharpasi / Urush Xudosi)</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "👁 Makima 👁")
async def makima_info(message: Message):
    media_id = "BAACAgIAAxkBAAIBymoX93UHbHqUpIQKJ--Gsh_LUzt8AAIkmAACtX3BSBb71FcyzaRFOwQ"
    caption_text = "<b>👁 Makima (Nazorat Iblisi)</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🔴 Dante")
async def dante_info(message: Message):
    media_id = "BAACAgIAAxkBAAIB0moX_KRN9mMkYtWa9emKnkPqeys9AAJTmAACtX3BSEZ8vljcGorIOwQ"
    caption_text = "<b>🔴 Dante (Afsonaviy Iblis Ovchisi)</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "❌ Arlecchino ❌")
async def arlecchino_info(message: Message):
    media_id = "BAACAgIAAxkBAAIB2GoX_evQOXaEQtmPSOtX9n2ZfplTAAJcmAACtX3BSCQZRySXFpr9OwQ"
    caption_text = "<b>❌ Arlecchino (The Knave)</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🤖 Connor")
async def connor_info(message: Message):
    media_id = "BAACAgIAAxkBAAIBumoX8K-EBh_AOJHUCEcf2a8BsWTUAAJwkwACnfRgS7j31D7cU-6YOwQ"
    caption_text = "<b>🤖 Connor (Model RK800)</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🥷 Noob Saibot")
async def noob_saibot_info(message: Message):
    media_id = "BAACAgIAAxkBAAIBamoUg8PbG4DtmRaX7CQB9FdtKpV7AAI3lwACjZKgSFhuggABOfEirTsE"
    caption_text = "<b>🥷 Noob Saibot (Bi-Han)</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "💀 Ghost")
async def ghost_info(message: Message):
    media_id = "BAACAgIAAxkBAAIBbGoUg8j92WWhKrTa3xV6heFEDGpnAAItlwACjZKgSLi5Zj507toFOwQ"
    caption_text = "<b>💀 Simon 'Ghost' Riley</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🦇 Batman")
async def batman_info(message: Message):
    media_id = "BAACAgIAAxkBAAIBaGoUg72Ms_9mgpBBLMvHXesjQEI5AAJDlwACjZKgSLGiVwmdJJTXOwQ"
    caption_text = "<b>🦇 Batman (Bruce Wayne)</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "📓 Light Yagami")
async def light_yagami_info(message: Message):
    media_id = "BAACAgIAAxkBAAIBZmoUg7etRptLAUnHvKke-XnHo9HPAAJOlwACjZKgSI7LDIy6w9VnOwQ"
    caption_text = "<b>📓 Light Yagami (Kira)</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🎬 Videolar bo'limi")
async def show_video_menu(message: Message):
    await message.answer("Qaysi videoni ko'rmoqchisiz?", reply_markup=video_kb)

@router.message(F.text == "🩸 Invincible")
async def invincible_info(message: Message):
    media_id = "BAACAgIAAxkBAAIByGoX93EsjUXwIBW_raltpMnOut2VAAInmAACtX3BSEK9q_1ZPU6rOwQ"
    caption_text = "<b>Why did you make me do this? You're fighting so that you can watch everyone around you die! Think, Mark!</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🦸‍♂️ The Boys")
async def the_boys_info(message: Message):
    media_id = "BAACAgIAAxkBAAIBNGoQZhwTRiim5VRuwE-JudxdKuf1AALxoAACxsoYSCP2RKrydXKSOwQ"
    caption_text = "<b>I'm the Homelander. And I can do whatever the fuck I want.</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "👻 Supernatural")
async def supernatural_info(message: Message):
    media_id = "BAACAgIAAxkBAAIBSGoQbg185GyMBxKfT6HZFX8_mQ1SAAJ9qAACUEOBSCMBpp48lIwyOwQ"
    caption_text = "<b>Saving people, hunting things. The family business.</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "⏳ Loki")
async def loki_info(message: Message):
    media_id = "BAACAgIAAxkBAAIBRmoQbgmapXywg_5HP9PzQcQ_qT7PAAJ6qAACUEOBSKnNogOlNU1cOwQ"
    caption_text = "<b>I know what kind of god I need to be. For you. For all of us.</b>"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🤠 Red Dead Redemption 2")
async def rdr2_info(message: Message):
    media_id = "BAACAgIAAxkBAAPqahBcNcnqf1nlc66SsONSntjWJ3gAApSnAAJQQ4FI0gYe3_qbMpc7BA"
    caption_text = "<b>We're thieves in a world that don't want us no more.</b> 🤠🍂"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🤖 Detroit: Become Human")
async def detroit_info(message: Message):
    media_id = "BAACAgIAAxkBAAPqahBcrzHfI16bCgGDsn-lWT5S8tYAAsN3AAJGuNlJmtn6zCsgU1o7BA"
    caption_text = (
        "<b>- And you know they have something I could never have.\n"
        "- Really? What's that?\n"
        "- A SOUL...</b> 🤖💙"
    )
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🌆 Cyberpunk 2077")
async def cyberpunk_info(message: Message):
    media_id = "BAACAgIAAxkBAAPsahBgWO-z5CKIUmMLa5hZyUzPpkMAAt6iAAK9q4hIaFckhy9657Q7BA"
    caption_text = "<b>Wake the fuck up, Samurai. We have a city to burn.</b> 🌆🎸"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "✨ Genshin Impact")
async def genshin_info(message: Message):
    media_id = "BAACAgIAAxkBAAPuahBg4zlLSk6ZS2ODJNUsVV5oaIcAAo6XAAIMyAFL-wLusr3VZWI7BA"
    caption_text = "<b>Agar qayta tanlov berilsa men yana seni tanlardim xuddi senga avval sarflagan 850 soat vaqtimdek...</b> ⏳❤️"
    try:
        await message.answer_video(video=media_id, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")

@router.message(F.text == "🎬 History L")
async def send_video_handler(message: Message):
    try:
        video_id = "BAACAgQAAxkBAAIC0GoftHToFlJg8b90xtF19sXRaJnBAAJVCwAC5ATUUMlHxP8xslPcOwQ"
        await message.answer_video(video=video_id, caption="Resident Evil qahramoni: Leon S. Kennedy! 🔥")
    except Exception as e:
        await message.answer(f"Video yuborishda xato: {e}")

@router.message(F.text == "🧾 Requiem")
async def send_raccoon_video(message: Message):
    video_id = "BAACAgIAAxkBAAICzmoftFyYJfPSgBknQl3LD-wSqLi2AAKLjwACI3_pSgp2Z4vllVaVOwQ"
    try:
        await message.answer_video(video=video_id, caption="<b>Dahshatli va unutilmas qaytish</b> 🔥", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Video yuborishda xato: {e}")

@router.message(F.text == "💀 Hunk")
async def send_hunk_video(message: Message):
    video_id = "BAACAgIAAxkBAAM6agVbMo7fY4Yno-l8zKmu5vnjvUUAAjORAAIjf-lKveABGuzJlzM7BA"
    try:
        await message.answer_video(video=video_id, caption="<b>Hunk:</b> 'This is war. Survival is your responsibility.' 🦾🔥", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Yuborishda xato: {e}")

@router.message(F.text == "🔬 Luis Sera")
async def send_luis_video(message: Message):
    video_id = "BAACAgIAAxkBAAICzGoftFM3YwSEOYDZSTc9aB6BHkoYAAK-lwACe6zBSgri7-jpEpvuOwQ"
    try:
        await message.answer_video(video=video_id, caption="<b>Luis Sera:</b> 'People can change right?' 🔬💉", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Yuborishda xato: {e}")

@router.message(F.text == "🎮 RE Evolution (1996-2026)")
async def send_re_evolution_video(message: Message):
    video_id = "BAACAgIAAxkBAAM8agVbN0bNwqZHgHl35McAATUPUwb5AAI2kQACI3_pSvmLN1tmoj-JOwQ"
    try:
        await message.answer_video(
            video=video_id,
            caption=(
                "<b>Resident Evil: 1996-yildan hozirgi kungacha!</b> 🔥\n\n"
                "Klassik qismlardan tortib, eng so'nggi Remake va yangi qismlargacha."
            ),
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"Video yuborishda xato: {e}")

@router.callback_query(F.data == "check_subscription")
async def check_btn(callback: CallbackQuery, bot: Bot):
    is_sub = await check_sub(bot, callback.from_user.id)
    if is_sub:
        await callback.message.delete()
        await callback.message.answer("Rahmat! Endi botdan foydalanishingiz mumkin.", reply_markup=main_kb)
    else:
        await callback.answer("Siz hali obuna bo'lmadingiz! ❌", show_alert=True)

@router.message(F.text == "🎮 Resident evilga kirish")
async def open_re_menu(message: Message):
    await message.answer("Resident Evil olami bo'yicha ma'lumot tanlang:", reply_markup=re_main_kb)

@router.message(F.text == "📖 Resident evil tarixi")
async def re_history(message: Message):
    history_text = (
        "<b>Resident Evil (Biohazard) To'liq Tarixi:</b>\n\n"
        "<b>1. Ibtido va Umbrella (1960-yillar):</b>\n"
        "Hamma narsa Afrikadagi qadimiy 'Soniq' guli va undan olingan 'Progenitor' virusi bilan boshlangan. "
        "Osvel Spenser va Edvard Ashford <b>Umbrella</b> korporatsiyasiga asos solishdi.\n\n"
        "<b>2. Raccoon City Fojiasi (1998):</b>\n"
        "Umbrellaning laboratoriyalarida virus tarqalib ketdi. S.T.A.R.S a'zolari Jill va Chris bu daxshatga guvoh bo'lishdi. "
        "Leon va Claire omon qolishga urinishdi, lekin oxiri shaharga yadroviy raketa tashlandi.\n\n"
        "<b>3. Global Tahdid:</b>\n"
        "Umbrella parchalangach, viruslar qora bozorga chiqdi. Chris Redfield BSAA tashkilotini tuzdi. "
        "Eng so'nggi sahifalar esa <b>Mother Miranda</b> va Qora mog'or bilan bog'liq."
    )
    await message.answer_photo(photo="https://pin.it/4gT9rKfle", caption=history_text)

@router.message(F.text == "🕹 Resident evil o'yinlari")
async def re_games_complete(message: Message):
    games_text = (
        "<b>Resident Evil O'yinlar Xronologiyasi (0-8):</b>\n\n"
        "• <b>RE 0 (Zero):</b> Hammasi qayerdan boshlangan? Rebecca va Billy Arklay tog'laridagi poyezdda Umbrella'ning birinchi sirini ochishadi.\n"
        "• <b>RE 1:</b> Jill va Chrisning klassik qasrdagi (Spencer Mansion) ilk to'qnashuvi va Veskerning xiyonati.\n"
        "• <b>RE 2:</b> Raccoon City apokalipsisi. Leon va Claire'ning shahardan qochishi va <b>Mr. X</b> ta'qibi.\n"
        "• <b>RE 3 Nemesis:</b> Jill Valentinening qochish missiyasi va uni o'ldirish uchun yuborilgan <b>Nemesis</b> bilan jangi.\n"
        "• <b>RE 4:</b> Leoning Ispaniyadagi missiyasi. 'Las Plagas' paraziti va Ada Wong bilan sirli uchrashuv yoritiladi.\n"
        "• <b>RE 5:</b> Chris Redfield Afrikada. Wesker bilan vulqon ichidagi so'nggi hal qiluvchi jang.\n"
        "• <b>RE 6:</b> Global bioterrorizm. Leon, Chris va Adaning yo'llari oxirgi marta kesishadi va ajraladi.\n"
        "• <b>RE 7 Biohazard:</b> Ethan Wintersning paydo bo'lishi. Beykerlar oilasidagi psixologik dahshat.\n"
        "• <b>RE 8 Village:</b> Ethanning qizini qutqarishi, Mother Miranda va Winterslar hikoyasining yakuni.\n"
    )
    await message.answer_photo(photo="https://pin.it/5n95LvUX3", caption=games_text)

@router.message(F.text == "🦸‍♂️ Resident evil qahramonlari")
async def show_heroes(message: Message):
    await message.answer("Qahramon haqida ma'lumot olish uchun tanlang:", reply_markup=heroes_kb)

@router.message(F.text == "Keyingi qahramonlar ➡️")
async def open_heros_page_2(message: Message):
    await message.answer("Qahramonlar (2-qism):", reply_markup=heroes_kb2)

@router.message(F.text == "Leon S. Kennedy")
async def hero_leon(message: Message):
    await message.answer_photo(
        photo="https://pin.it/6cSF9zTAn",
        caption=(
            "<b>Leon S. Kennedy:</b>\n\n"
            "1998-yilda Raccoon City politsiya mahkamasiga ishga kirgan kuniyoq shahar zombi apokalipsisiga yuz tutdi. Aynan shu yerda u birinchi marta <b>Ada Wong</b> bilan to'qnash keldi. U paytda Ada oddiy fuqaro deb o'ylangan bo'lsa-da, keyinchalik u josus ekani ma'lum bo'ldi.\n\n"
            "Resident Evil 4 voqealarida ular yana kesishdi. Leon Ispaniyadagi qishloqda qizni qutqarish uchun kurashar ekan, Ada uning yo'lini doimiy ravishda kesib o'tib, o'zining yashirin maqsadlarini amalga oshirayotgan edi. "
            "Resident Evil 6 da esa vaziyat keskinlashdi: ularning yo'llari endi bir-biriga qarshi ishlaydigan tashkilotlar orqali ajraldi. Leon o'z missiyasini bajarishda davom etdi, Ada esa o'zining sirli o'tmishi bilan bog'liq bo'lgan yangi tahdidlarga qarshi chiqdi. "
            "Leoning Adaga bo'lgan shubhalari va nima uchun uni har safar tirik qoldirishi haqidagi savollarga Ada qanday javob berishi uning o'z bo'limida yoritilgan."
        )
    )

@router.message(F.text == "Ada Wong")
async def hero_ada(message: Message):
    await message.answer_photo(
        photo="https://pin.it/3EW9Oxsdb",
        caption=(
            "<b>Ada Wong:</b>\n\n"
            "Raccoon City'dagi voqealardan buyon Ada soyalarda qolishni tanlagan josus. Leon bilan birinchi marta o'sha dahshatli shaharda uchrashganda, u Leonni shunchaki o'z maqsadiga yetishish uchun vosita deb hisoblagan edi.\n\n"
            "RE4 davomida Ada Leonning harakatlarini kuzatib bordi va kerakli paytda unga yordam berib, o'zi uchun virus namunalarini yig'ib yurdi. U hech qachon Leonning yashash tarzini tushunmagan, Leon esa uning ishlarini hech qachon oqlamagan. "
            "RE6 voqealarida ularning qarashlari va vazifalari butkul qarama-qarshi tomonga o'zgardi — ular endi ittifoqchi emas, balki turli manfaatlarga ega ikki alohida taraf edi. Bu bosqichda ularning yo'llari oxirgi marta ajraldi. "
            "Adaning nima uchun RE6'da Leon bilan birga bo'lishdan voz kechgani va nega aynan shu vaqtda ajralishni tanlagani haqidagi aniq motivatsiyalar Leonning voqealar davomidagi qarorlarida o'z aksini topgan."
        )
    )

@router.message(F.text == "Chris Redfield")
async def hero_chris(message: Message):
    await message.answer_photo(
        photo="https://pin.it/59SLZ8U9R",
        caption=(
            "<b>Chris Redfield:</b>\n\n"
            "S.T.A.R.S a'zosi va BSAA asoschisi. Chrisning butun hayoti bitta inson — <b>Albert Wesker</b> bilan bog'liq. 1998-yilda qasrdagi (RE1) voqealarda Wesker o'z jamoasiga xiyonat qilganidan so'ng, Chris uni to'xtatishni o'zining hayotiy maqsadiga aylantirdi.\n\n"
            "Ular bir necha bor to'qnash kelishdi: 'Rockfort' orolida (Code: Veronica) Wesker g'ayriinsoniy kuchga ega bo'lib qaytganida, Chris uning naqadar xavfli ekanini tushunib yetdi. Ularning 10 yillik adovati 2009-yilda Afrikada (RE5) cho'qqisiga chiqdi. Chris o'zining sherigi Sheva bilan birga, Weskerni dunyoni Uroboros virusi bilan yo'q qilish rejasini barbod qildi va uni faol vulqon ichida yo'q qildi.\n\n"
            "Weskerdan keyin Chris o'zini yo'qotib qo'ygandek bo'ldi, ammo RE7 va RE8da u <b>Ethan Winters</b>ning himoyachisiga aylandi. Chris Ethanning matonatini ko'rib, unda o'zining yoshligini ko'rdi. Chrisning nima uchun Winterslar oilasini o'z himoyasiga olgani va Ethanga bergan so'nggi va'dasi haqida Ethan bo'limida batafsil ma'lumot bor."
        )
    )

@router.message(F.text == "Ethan Winters")
async def hero_ethan(message: Message):
    ethan_photo = "https://pin.it/1IdH7RSVv"
    await message.answer_photo(
        photo=ethan_photo,
        caption=(
            "<b>Ethan Winters: Oddiy inson, buyuk qahramon</b>\n\n"
            "Ethan — Resident Evil olamidagi eng g'ayritabiiy va irodali qahramon. U maxsus tayyorgarlikdan o'tgan agent emas, shunchaki o'z oilasini qutqarish uchun jahannamga kirib borishga tayyor bo'lgan ota. Uning tanasi mog'or (Mold) bilan zararlangan bo'lsa-da, o'z yaqinlarini himoya qilish uchun foydalandi.\n\n"
            "RE8 boshida Ethan Chrisni dushman deb bildi, chunki Chris uning ko'z o'ngida xotiniga qarata o'q uzgan edi. Ammo Ethan bu tushunmovchilikka qaramay, Chris bilan birga Mirandaning lordlarini yo'q qilishda va qizini qutqarishda yelkama-yelka turib jang qildi.\n\n"
            "Ethan Mirandani yengish uchun o'z hayotini tikdi. Miranda uning qalbini sug'urib olganida ham, Ethan o'z irodasi va mog'or kuchi bilan o'limni orqaga surdi. U Mirandaning barcha mutatsiyalariga qarshi oxirigacha kurashib, uni butkul yo'q qildi.\n\n"
            "<i>Mening shaxsiy fikrimcha, Ethan Winters rost qahramondir. Chunki u burch yuzasidan emas, insoniy muhabbat va fidoyilik uchun o'limni tanladi.</i>"
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Jill Valentine")
async def hero_jill(message: Message):
    jill_status = "<i>\"You want S.T.A.R.S.? I'll give you S.T.A.R.S.!\"</i>"
    photo_url = "https://pin.it/76wTuLVp9"
    await message.answer_photo(
        photo=photo_url,
        caption=(
            f"<b>Jill Valentine:</b>\n\n"
            f"S.T.A.R.S. maxsus bo'linmasining mahoratli a'zosi va portlovchi moddalar bo'yicha mutaxassis. "
            f"Uning hayotidagi eng dahshatli sinov 1998-yilda Raccoon City ko'chalarida boshlangan. Jill shaharni tark etishga urinarkan, "
            f"uni Umbrella korporatsiyasi tomonidan yuborilgan dahshatli <b>Nemesis</b> tinimsiz ta'qib qildi.\n\n"
            f"Jill shunchaki qochib qutulishni emas, balki bu maxluqni butkul yo'q qilishni maqsad qilgan edi. "
            f"U Nemesis bilan bir necha marta yuzma-yuz keldi: politsiya mahkamasida, soat minorasida va nihoyat zavodda. "
            f"Jill o'zining tezkorligi va aql-idroki bilan Nemesisning barcha shakllarini mag'lub etib, shahar yadroviy raketa bilan "
            f"yo'q qilinishidan bir necha soniya oldin uni Railgun quroli bilan parchalab tashladi.\n\n"
            f"{jill_status}\n\n"
            f"Jillning bu g'alabasi uning irodasini isbotladi. Nemesis nima uchun aynan uni nishonga olgani haqida "
            f"<b>Yovuzlar</b> bo'limidagi Nemesis ta'rifida batafsil o'qishingiz mumkin."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Claire Redfield")
async def hero_claire(message: Message):
    await message.answer_photo(
        photo="https://pin.it/ssqJZko6x",
        caption=(
            "<b>Claire Redfield:</b>\n\n"
            "Chrisning singlisi. Akasini izlab kelib, yetim qolgan <b>Sherry Birkin</b>ni qutqarishni burchiga aylantirdi. "
            "Claire va Sherryni to'xtatish uchun yuborilgan <b>Mr. X</b>ni jasorati bilan yengib o'tdi. "
            "U professional askar bo'lmasa-da, oddiy talaba qiz qanday qilib yovuzlardan ustun kelishini isbotladi."
        )
    )

@router.message(F.text == "Mia Winters")
async def heros_mia(message: Message):
    mia_photo = "https://pin.it/54dAyrAle"
    await message.answer_photo(
        photo=mia_photo,
        caption=(
            "<b>Mia Winters:</b>\n\n"
            "Mia — Ethan Wintersning rafiqasi. U uzoq vaqt davomida oddiy enaga bo'lib ishlashini aytib, "
            "aslida 'The Connections' nomli maxfiy tashkilotda ishlayotganini yashirgan. U Eveline'ni "
            "tashish operatsiyasi paytida halokatga uchrab, 3 yil davomida Bakerlar oilasida asir bo'lib qolgan.\n\n"
            "<b>Xususiyati:</b> U Eveline'ning mog'ori (Mold) bilan zararlangan, shuning uchun ba'zida "
            "o'zini nazorat qila olmay qoladi va tajovuzkor bo'lib qoladi. Ethan uni qutqarish uchun "
            "hamma narsaga tayyor bo'ladi."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Zoe Baker")
async def hero_zoe(message: Message):
    zoe_photo = "https://pin.it/3APAtHp4C"
    await message.answer_photo(
        photo=zoe_photo,
        caption=(
            "<b>Zoe Baker:</b>\n\n"
            "Zoe — Bakerlar oilasining qizi. U o'z oilasining aqldan ozganidan so'ng, ulardan alohida, "
            "hovlidagi vagonda yashaydi. U oila a'zolari kabi butkul aqldan ozmagan va Ethanga "
            "bu jahannamdan qochish uchun yordam beradi.\n\n"
            "<b>Rolli:</b> Zoe shifobaxsh zardob (Serum) tayyorlashni biladi. U o'zi ham mog'or bilan "
            "zararlangan, lekin uning irodasi juda kuchli. Uning qismati o'yindagi tanlovingizga "
            "bog'liq (Zardobni unga berasizmi yoki Miagami)."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Sherry Birkin")
async def hero_sherry(message: Message):
    sherry_photo = "https://pin.it/WAkStQkDv"
    await message.answer_photo(
        photo=sherry_photo,
        caption=(
            "<b>Sherry Birkin:</b>\n\n"
            "Sherry — G-virus yaratuvchisi William Birkinning qizi. Bolaligida Claire Redfield uni qutqarib qolgan edi. "
            "RE6 davrida u BSAA maxsus agenti sifatida ishlaydi.\n\n"
            "<b>Xususiyati:</b> Uning tanasida qolgan G-virus qoldiqlari unga tez tiklanish qobiliyatini bergan. "
            "Uning vazifasi — Jake Mullerning qonidagi antitanalarni saqlab qolish va dunyoni C-virusidan qutqarish."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Rebecca Chambers")
async def hero_rebecca(message: Message):
    rebecca_photo = "https://pin.it/6Qz3IDSMr"
    await message.answer_photo(
        photo=rebecca_photo,
        caption=(
            "<b>Rebecca Chambers:</b>\n\n"
            "Rebecca — S.T.A.R.S. maxsus bo'linmasining eng yosh a'zosi (atigi 18 yoshda bo'limga qo'shilgan). "
            "U kimyo va tibbiyot bo'yicha daho hisoblanadi. Resident Evil 0 o'yinida u Billy Coen bilan birga "
            "Umbrella'ning birinchi sirli laboratoriyasini ochgan.\n\n"
            "<b>Xususiyati:</b> U jangchi emas, ko'proq yordamchi (medic) vazifasini bajaradi. RE1 o'yinida "
            "Chris Redfieldning hayotini bir necha bor saqlab qolgan. Hozirda u universitet professori va "
            "viruslarga qarshi vaksina yaratish ustida ishlaydigan olima."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Jake Muller")
async def hero_jake(message: Message):
    jake_photo = "https://pin.it/6SG7iXxBG"
    await message.answer_photo(
        photo=jake_photo,
        caption=(
            "<b>Jake Muller:</b>\n\n"
            "Jake — Albert Weskerning o'g'li. U o'z hayotini yollanma askar sifatida o'tkazgan va hech kimga ishonmaydi. "
            "U o'z otasining kimligini bilmagan, lekin uning qonida virusga qarshi tabiiy immunitet bor.\n\n"
            "<b>Xususiyati:</b> Jake judayam kuchli va jang san'atlarini a'lo darajada biladi. Uning Sherry Birkin bilan "
            "bo'lgan munosabati o'yin davomida o'zgarib boradi: yolg'iz yovuz odamdan, dunyoni qutqaruvchi qahramonga aylanadi."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "🦹‍♂️ Resident evil yovuzlari")
async def show_villains(message: Message):
    await message.answer("Yovuzlar haqida ma'lumot olish uchun tanlang:", reply_markup=villains_kb1)

@router.message(F.text == "Keyingi yovuzlar ➡️")
async def open_villains_page_2(message: Message):
    await message.answer("Yovuzlar (2-qism):", reply_markup=villains_kb2)

@router.message(F.text == "Albert Wesker")
async def villain_wesker(message: Message):
    wesker_speech = "<i>\"Seven minutes. Seven minutes is all I can spare to play with you.\"</i>"
    photo_url = "https://pin.it/1hzKySBiN"
    await message.answer_photo(
        photo=photo_url,
        caption=(
            f"<b>Albert Wesker:</b>\n\n"
            f"Wesker — nafaqat Umbrella agenti, balki butun insoniyatni 'saralash' va o'zi yangi dunyo xudosi bo'lishni istagan daho. "
            f"U 1998-yilda S.T.A.R.S. komandiri sifatida o'z jamoasiga (Chris va Jillga) xiyonat qildi va o'z o'limini sahnalashtirib, "
            f"tanasiga maxsus virus yubordi. Bu unga g'ayriinsoniy tezlik va kuch berdi.\n\n"
            f"<b>Nega aynan 7 minut?</b>\n"
            f"Resident Evil 5 o'yinidagi mashhur jangda Wesker Chris va Shevaga qarata: {wesker_speech} degan jumlani aytadi. "
            f"Bu uning kibridan dalolat: u o'zini shunchalik ustun deb biladiki, raqiblarini yo'q qilish uchun bor-yo'g'i 7 daqiqa kifoya deb hisoblaydi. "
            f"Weskerning Chris Redfield bilan bo'lgan 10 yillik adovati nafaqat nafratga, balki bir-birini dunyodagi yagona munosib raqib deb bilishiga asoslangan. "
            f"Weskerning mag'lubiyati va vulqon ichidagi so'nggi daqiqalari haqida Chris Redfield bo'limida yana bir bor eslatib o'tilgan."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Mr. X")
async def villain_mrx(message: Message):
    await message.answer_photo(
        photo="https://pin.it/5jKrA3H4s",
        caption=(
            "<b>Mr. X (T-00):</b>\n\n"
            "Umbrella tomonidan Raccoon City politsiya mahkamasiga (RPD) yuborilgan sovuqqon va tinimsiz ta'qibchi. Uning vazifasi — epidemiyadan tirik qolgan barcha guvohlarni yo'q qilish va virus namunalarini yig'ish edi. Mr. X ayniqsa <b>Claire Redfield</b> va Sherry Birkinning ortidan soya kabi yurib, ularni o'lim yoqasiga olib keldi.\n\n"
            "U hech qachon charchamaydi, gapirmaydi va o'z nishonini topmaguncha to'xtamaydi. Uning og'ir qadam tovushlari Claire uchun dahshatli xabarchi edi. Claire o'zining chaqqonligi va Sherryga bo'lgan g'amxo'rligi sababli bu maxluqdan bir necha bor qochib qutulishga erishdi."
        )
    )

@router.message(F.text == "Nemesis")
async def villain_nemesis(message: Message):
    await message.answer_photo(
        photo="https://pin.it/PHq6ttjb4",
        caption=(
            "<b>Nemesis (Pursuer):</b>\n\n"
            "Umbrella korporatsiyasi tomonidan yaratilgan eng mukammal va aqlli biologik qurol. Uning yagona va qat'iy dasturi bor edi: Raccoon City politsiyasining barcha S.T.A.R.S. a'zolarini topish va yo'q qilish. Nemesis boshqa Tirantlardan farqli o'laroq, gapirishni (uning mashhur 'S.T.A.R.S...' hayqirig'i) va og'ir qurollardan foydalanishni bilar edi.\n\n"
            "U <b>Jill Valentine</b>ni shahar bo'ylab o'lim soyasi kabi ta'qib qildi. Jill uni har safar mag'lub etganida, Nemesis yangi va yanada dahshatliroq shaklga kirib, qayta tiklanaverdi. Ammo uning butun kuch-qudrati Jillning irodasi oldida ojiz qoldi."
        )
    )

@router.message(F.text == "Mother Miranda")
async def villain_miranda(message: Message):
    miranda_speech = "<i>\"O'sha kundan boshlab men o'limni yengish yo'lini qidirdim... va uni topdim.\"</i>"
    photo_url = "https://pin.it/4RiijJLEb"
    await message.answer_photo(
        photo=photo_url,
        caption=(
            f"<b>Mother Miranda:</b>\n\n"
            f"Miranda — 100 yildan ortiq vaqt davomida yashab kelayotgan, qishloqni 'Megamycete' (Qora mog'or) yordamida nazorat qiluvchi yetakchi. "
            f"Uning butun hayoti 1919-yilda vafot etgan qizi Evani qayta tiriltirishga yo'naltirilgan.\n\n"
            f"<b>Umbrella bilan bog'liqligi:</b>\n"
            f"Umbrella asoschisi Osvel Spenser yoshligida Mirandaning shogirdi bo'lgan. Spenser viruslar orqali evolyutsiyani, "
            f"Miranda esa mog'or orqali tiriltirishni istagan. Hatto Umbrella logotipi ham shu qishloqdagi qadimiy belgidan olingan.\n\n"
            f"<b>Ethan Winters bilan to'qnashuv:</b>\n"
            f"Miranda qizi uchun 'mukammal tana' sifatida Ethanning qizi Rozmarini o'g'irlaydi. U o'z shaklini o'zgartira oladi — "
            f"hatto Mia ko'rinishida Ethanning uyiga kirgan. U o'zining to'rtta 'farzandi'ni (Dimitresku, Heisenberg va b.) shunchaki vosita deb bilgan.\n\n"
            f"{miranda_speech}\n\n"
            f"Mirandaning Ethan bilan so'nggi jangi va Chris Redfieldning roli haqida <b>Ethan Winters</b> bo'limida tanishishingiz mumkin."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Krauser")
async def villain_krauser(message: Message):
    await message.answer_photo(
        photo="https://pin.it/1smQLAMiO",
        caption=(
            "<b>Jack Krauser:</b>\n\n"
            "Krauser — Leoning sobiq ustozi va sherigi. U o'z vaqtida AQSH maxsus kuchlarida xizmat qilgan mahoratli askar edi. "
            "Biroq, operatsiyalardan birida og'ir yaralanib, o'zining kuchsizligini his qiladi va g'ayritabiiy kuchga ega bo'lish uchun "
            "Saddler va Wesker bilan hamkorlik qiladi.\n\n"
            "<b>Asosiy xususiyati:</b> U pichoq bilan jang qilish ustasi. Mutatsiyaga uchraganda uning chap qo'li bahaybat, "
            "keskir va o'q o'tmas pichoq-qalqonga aylanadi. U Leonni doim 'kursant' (rookie) deb chaqiradi."
        )
    )

@router.message(F.text == "Ramon Salazar")
async def villain_salazar(message: Message):
    salazar_photo = "https://pin.it/6mw3qBNEi"
    await message.answer_photo(
        photo=salazar_photo,
        caption=(
            "<b>Ramon Salazar:</b>\n\n"
            "Salazar — Ispaniyadagi qadimiy qasrning 8-egasi. U tashqi ko'rinishidan qari cholga o'xshasa-da, aslida yoshi atigi 20 larda. "
            "Uning oilasi asrlar davomida 'Las Plagas' parazitini qasr ostida yashirib kelgan.\n\n"
            "<b>Rolli:</b> Saddlerning ta'siri ostida u Leon va Ashleyning yo'liga to'sqinlik qiladi. Uning ikkita bahaybat qo'riqchisi "
            "(Verdugo) bor. Mutatsiya holatida u qasr devorlari bilan birlashib, ulkan, bir ko'zli maxluqqa aylanadi."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Jack Baker")
async def villain_jack(message: Message):
    jack_photo = "https://pin.it/5AXI7rMn4"
    await message.answer_photo(
        photo=jack_photo,
        caption=(
            "<b>Jack Baker:</b>\n\n"
            "Jack — Bakerlar oilasining boshlig'i va Ethan Wintersning RE7 dagi eng asosiy ta'qibchisi. "
            "U aslida mehribon ota va fermer bo'lgan, biroq Eveline tomonidan mog'or (Mold) bilan zararlangach, "
            "aqldan ozgan va o'ta shafqatsiz maxluqqa aylangan.\n\n"
            "<b>Xususiyati:</b> U deyarli o'lmas. Uni otish, mashina bilan urish yoki yoqib yuborish foyda bermaydi, "
            "chunki uning tanasi juda tez tiklanadi. Uning mashhur jumlasi: <i>'Welcome to the family, son!'</i>"
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "Eveline")
async def villain_eveline(message: Message):
    eveline_photo = "https://pin.it/2auqUTUWP"
    await message.answer_photo(
        photo=eveline_photo,
        caption=(
            "<b>Eveline:</b>\n\n"
            "Eveline — maxsus laboratoriyada yaratilgan biologik qurol. Uning maqsadi odamlarni mog'or "
            "yordamida boshqarish va o'zi uchun 'oila' yaratishdir. U Bakerlar oilasini aynan shu maqsadda "
            "o'ziga bo'ysundirgan.\n\n"
            "<b>Siri:</b> Eveline yosh qiz ko'rinishida bo'lsa-da, u juda tez qariydi. RE7 o'yini davomida "
            "biz ko'rgan nogironlar aravachasidagi kampir — aslida Eveline bo'lib chiqadi. U odamlarning "
            "miyasiga gallyutsinatsiyalar yuborish orqali ularni aqldan ozdiradi."
        ),
        parse_mode="HTML"
    )

@router.message(F.text == "💰 Resident evil budjeti")
async def re_budget_facts(message: Message):
    budget_text = (
        "<b>Resident Evil: Moliyaviy Faktlar va Budjet</b>\n\n"
        "<b>1. Ishlab chiqarish xarajatlari:</b>\n"
        "Resident Evil o'yinlari 'AAA' (top darajadagi) loyihalar hisoblanadi. Masalan, <b>Resident Evil 6</b> o'yinini yaratish uchun Capcom 600 dan ortiq xodimni jalb qilgan. O'rtacha hisobda zamonaviy qismlar (RE7, RE8, RE4 Remake) ishlab chiqilishi va marketingi uchun <b>$50 mln dan $100 mln gacha</b> mablag' sarflanadi.\n\n"
        "<b>2. Eng ko'p sotilgan qismlar:</b>\n"
        "Seriyaning umumiy savdosi 150 million nusxadan oshib ketgan. Eng muvaffaqiyatli qismlar:\n"
        "• <b>Resident Evil 5:</b> 14.6 mln nusxa.\n"
        "• <b>Resident Evil 2 Remake:</b> 13.1 mln nusxa.\n"
        "• <b>Resident Evil 7:</b> 12.4 mln nusxa.\n\n"
        "<b>3. RE Engine texnologiyasi:</b>\n"
        "Capcom budjetni tejash va sifatni oshirish uchun o'zining shaxsiy 'RE Engine' motorini yaratdi. Bu texnologiya o'yinlarni ishlab chiqish vaqtini qisqartirdi va grafikani realizm cho'qqisiga olib chiqdi.\n\n"
        "<b>4. Kino va Media daromadi:</b>\n"
        "Resident Evil filmlari dunyo bo'ylab kassada <b>$1.2 milliarddan</b> ortiq mablag' to'plagan. Bu Resident Evil'ni tarixdagi eng muvaffaqiyatli videoo'yin asosidagi kinofranshizaga aylantirdi.\n\n"
        "<i>Xulosa: Resident Evil — bu Capcom uchun har yili yuzlab million dollar foyda keltiradigan, barqaror va o'ta qimmat brenddir.</i>"
    )
    await message.answer(text=budget_text, parse_mode="HTML")

@router.message(F.text == "⬅️ RE Menyuga qaytish")
async def back_to_re(message: Message):
    await message.answer("Resident Evil bo'limiga qaytdingiz:", reply_markup=re_main_kb)

@router.message(F.text == "⬅️ Ortga")
async def back_home(message: Message):
    await message.answer("Bosh menyuga qaytdingiz:", reply_markup=main_kb)

@router.message(F.text)
async def smart_search(message: Message):
    text = message.text.lower()
    if "leon" in text:
        await hero_leon(message)
    elif "ada" in text:
        await hero_ada(message)
    elif "chris" in text:
        await hero_chris(message)
    elif "ethan" in text:
        await hero_ethan(message)
    elif "jill" in text:
        await hero_jill(message)
    elif "claire" in text:
        await hero_claire(message)
    elif "mia" in text:
        await heros_mia(message)
    elif "zoe" in text:
        await hero_zoe(message)
    elif "sherry" in text:
        await hero_sherry(message)
    elif "jake" in text:
        await hero_jake(message)
    elif "rebecca" in text:
        await hero_rebecca(message)
    elif "wesker" in text:
        await villain_wesker(message)
    elif "mr. x" in text or "mrx" in text:
        await villain_mrx(message)
    elif "nemesis" in text:
        await villain_nemesis(message)
    elif "miranda" in text:
        await villain_miranda(message)
    elif "krauser" in text:
        await villain_krauser(message)
    elif "salazar" in text:
        await villain_salazar(message)
    elif "jack" in text:
        await villain_jack(message)
    elif "eveline" in text:
        await villain_eveline(message)
    else:
        await message.answer("🤖 <i>AI javob tayyorlanmoqda...</i>", parse_mode="HTML")
        javob = ask_gemini(message.text)
        if javob:
            await message.answer(f"🤖 <b>AI javob:</b>\n\n{javob}", parse_mode="HTML")
        else:
             try:
                wiki_info = wikipedia.summary(message.text, sentences=5)
                await message.answer(f"📚 <b>Wikipedia:</b>\n\n{wiki_info}", parse_mode="HTML")
             except Exception:
                await message.answer("❌ Kechirasiz, ma'lumot topilmadi.")

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    print("Bot Gemini AI bilan ishga tushdi! ✨")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
