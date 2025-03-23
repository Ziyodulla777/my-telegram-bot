import telebot
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ✅ Bot tokeningizni kiritishingiz kerak
TOKEN = "7551121878:AAFeAnkUkWmzLTLu7ZgpeIc5lPYc3Zz5MCY"
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")  # Markdown qo‘shildi

# ✅ Kanal ma'lumotlari
CHANNEL_USERNAME = "@xbet_linebet_stavk"  # Public kanal username (oldin @ belgisi bo‘lishi shart!)
CHANNEL_LINK = "https://t.me/xbet_linebet_stavk"  # Kanal havolasi

# ✅ Rasm fayllari to‘g‘ri joylashgan
IMAGE_FILES = {
    1: "1.png",
    2: "2.png",
    3: "3.png",
    4: "4.png",
    5: "5.png",
}

# ✅ Bot ishga tushganligini ko‘rsatish
print("✅ *Bot ishga tushdi*")

# ✅ Kanalga obuna bo‘lganligini tekshirish (Tuzatildi!)
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        status = member.status
        print(f"👤 {user_id} - {status}")  # Log uchun
        return status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"❌ *Obuna tekshirishda xatolik:* {e}")
        return False

# ✅ Start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if is_subscribed(user_id):
        bot.send_message(user_id, "✅ *Siz allaqachon kanalga obuna bo‘lgansiz!*")
        send_apk_info(user_id)
        send_signal_menu(user_id)
    else:
        send_subscription_prompt(user_id)

# ✅ Obuna bo‘lish so‘rovini jo‘natish
def send_subscription_prompt(user_id):
    markup = InlineKeyboardMarkup()
    
    btn_subscribe = InlineKeyboardButton("📢 *Kanalga o'tish*", url=CHANNEL_LINK)
    btn_check = InlineKeyboardButton("✅ *Obuna bo‘ldim*", callback_data="check_subscription")

    markup.add(btn_subscribe)
    markup.add(btn_check)
    
    bot.send_message(user_id, "🔔 *Iltimos, kanalga obuna bo‘ling!*\n\n👇 *Kanalga kirish uchun pastdagi tugmani bosing:*", reply_markup=markup)

# ✅ Obuna tekshirish tugmasi (Tuzatildi!)
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_id = call.message.chat.id
    if is_subscribed(user_id):
        bot.send_message(user_id, "✅ *Tabriklaymiz! Siz kanalga obuna bo‘ldingiz!*")
        send_apk_info(user_id)
        send_signal_menu(user_id)
    else:
        bot.send_message(user_id, f"❌ *Siz hali ham kanalga obuna bo‘lmadingiz!*\n\n📢 *Kanalga o'tish uchun:* [Kanalga kirish]({CHANNEL_LINK})")

# ✅ APK va video qo‘llanma haqida ma’lumot
def send_apk_info(user_id):
    text = """📌 **1XBET dasturidan foydalanish uchun APK yuklab oling!**

🤖 **1XBET VZLOM dasturi faqat ushbu APK orqali ishlaydi!**
📥 **APK yuklab olish:** 👉 [Yuklab olish](https://t.me/lambo_bonus/32)
🎥 **Video qo‘llanma:** 👉 [Ko‘rish](https://t.me/lambo_bonus/29)

❗ **ESLATMA**  
*Agar tepada ko‘rsatilgan bosqichlarni to‘liq bajarmasdan signal olishni boshlasangiz, bot sizga to‘g‘ri signal bermaydi!*
"""
    bot.send_message(user_id, text)

# ✅ "Signal olish" tugmasini qo‘shish
def send_signal_menu(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_signal = KeyboardButton("📡 *Signal olish*")
    markup.add(btn_signal)
    bot.send_message(user_id, "📡 *Signal olish uchun tugmani bosing!*", reply_markup=markup)

# ✅ "Signal olish" tugmasi bosilganda tasodifiy rasm va yozuv yuborish
@bot.message_handler(func=lambda message: message.text == "📡 *Signal olish*")
def send_random_signal(message):
    user_id = message.chat.id
    random_number = random.randint(1, 5)
    image_path = IMAGE_FILES.get(random_number)

    if image_path:
        with open(image_path, "rb") as img:
            bot.send_photo(user_id, img, caption=f"📡 **Signal:** `{random_number}`")
    else:
        bot.send_message(user_id, "❌ *Rasm topilmadi!*")

# ✅ Botni ishga tushirish
bot.polling(none_stop=True)
