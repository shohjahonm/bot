# 1139713731  
# 8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4
import csv
import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    PollAnswerHandler, 
    ContextTypes
)

# 🔐 Sozlamalar
TOKEN = "8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4"  # <-- O'zingizning token
ADMIN_ID = 1139713731  # <-- O'zingizning admin ID

# CSV fayl
CSV_FILE = "results.csv"

# Foydalanuvchidan holatni saqlash
user_state = {}

# -------------------------
# CSV ga saqlash funksiyasi
# -------------------------
def save_result_csv(user_id, username, question, answers):
    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["user_id", "username", "question", "answers"])
        writer.writerow([user_id, username, question, ", ".join(answers)])

# -------------------------
# /start komandasi
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📨 Taklif va shikoyatlar")],
        [KeyboardButton("📊 So‘rovnomada qatnashish")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"☕️ Assalomu alaykum, {update.effective_user.first_name}!\n\n"
        "Aristocrat Cafe botiga xush kelibsiz! 😊\n"
        "Quyidagi menyudan kerakli bo‘limni tanlang:",
        reply_markup=reply_markup
    )

# -------------------------
# Foydalanuvchi xabarlarini boshqarish
# -------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == "📨 Taklif va shikoyatlar":
        user_state[chat_id] = "feedback"
        await context.bot.send_message(chat_id, "Iltimos, o‘z taklif yoki shikoyatingizni yozib qoldiring ☕️:")

    elif text == "📊 So‘rovnomada qatnashish":
        await send_polls(update, context)

    elif chat_id in user_state and user_state[chat_id] == "feedback":
        # Adminga yuborish
        await context.bot.send_message(ADMIN_ID, f"📩 Yangi fikr:\n\n{text}")
        await context.bot.send_message(chat_id, "Rahmat! Sizning fikringiz biz uchun muhim 💬")

        # Asosiy menyuga qaytish
        del user_state[chat_id]
        await start(update, context)

    else:
        await start(update, context)

# -------------------------
# So‘rovnomalarni yuborish
# -------------------------
async def send_polls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    polls = [
        {
            "question": "Bizning xizmat sifati sizni qoniqtirdimi?",
            "options": ["Ha, juda yaxshi", "O‘rtacha", "Yo‘q, yaxshilash kerak"]
        },
        {
            "question": "Kafelarimizdagi muhit sizga yoqdimi?",
            "options": ["Ha, ajoyib!", "Yaxshi", "Yoqmadi"]
        },
        {
            "question": "Narxlar darajasi haqida fikringiz?",
            "options": ["Arzon", "Mos", "Qimmat"]
        },
        {
            "question": "Siz bizni boshqalarga tavsiya qilarmidingiz?",
            "options": ["Ha, albatta", "Ehtimol", "Yo‘q"]
        },
    ]

    for poll in polls:
        msg = await context.bot.send_poll(
            chat_id=chat_id,
            question=poll["question"],
            options=poll["options"],
            is_anonymous=False,
            allows_multiple_answers=True
        )
        # Poll ma'lumotlarini saqlaymiz
        context.bot_data[msg.poll.id] = {"question": poll["question"], "options": poll["options"]}

    await context.bot.send_message(chat_id, "☕️ So‘rovnoma tugadi! Javoblaringiz uchun katta rahmat 💛")
    await start(update, context)

# -------------------------
# Poll javoblarini qayta ishlash
# -------------------------
async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user_id = answer.user.id
    username = answer.user.first_name
    poll_id = answer.poll_id
    selected = answer.option_ids

    poll_data = context.bot_data.get(poll_id)
    if poll_data:
        question = poll_data["question"]
        options = poll_data["options"]
        selected_text = [options[i] for i in selected]

        # Adminga yuborish
        await context.bot.send_message(
            ADMIN_ID,
            f"🗳 So‘rovnoma javobi:\n\n"
            f"👤 Foydalanuvchi: {username}\n"
            f"❓ Savol: {question}\n"
            f"✅ Javob: {', '.join(selected_text)}"
        )

        # CSV ga saqlash
        save_result_csv(user_id, username, question, selected_text)

# -------------------------
# Asosiy funksiya
# -------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(PollAnswerHandler(handle_poll_answer))

    print("🤖 Aristocrat Cafe bot ishga tushdi...")
    app.run_polling()

# -------------------------
if __name__ == "__main__":
    main()
