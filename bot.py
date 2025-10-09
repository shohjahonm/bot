# 1139713731   969555465
# 8328899370:AAG99a7wOhWT9noWihwuSEb2ccIhP825Fyo
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# 🔐 Bot token va admin ID lar
TOKEN = "8328899370:AAG99a7wOhWT9noWihwuSEb2ccIhP825Fyo"
ADMIN_IDS = [969555465, 1139713731]  # bu yerga 2ta admin ID yoz

# 🔢 So‘rovnoma savollari
polls = [
    {
        "question": "1️⃣ Sizga qaysi ovqatlar yoqadi?",
        "options": ["Manti", "Tovuq kabob", "Grechka", "Osh", "Lag'mon", "Go‘lupsi"]
    },
    {
        "question": "2️⃣ Qaysi sport turini yoqtirasiz?",
        "options": ["Futbol", "Basketbol", "Tennis", "Suzish", "Boks"]
    },
    {
        "question": "3️⃣ Siz ko‘proq qaysi paytda ishlaysiz?",
        "options": ["Ertalab", "Kunduzi", "Kechasi"]
    },
    {
        "question": "4️⃣ Sizda internet tezligi qanday?",
        "options": ["Yuqori", "O‘rta", "Past"]
    },
]

# 💾 Foydalanuvchi javoblarini saqlash
user_answers = {}


# 🟢 /start
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_answers[user_id] = {}
    context.user_data["poll_index"] = 0
    send_poll(update, context, 0)


# 📩 So‘rovnoma yuborish
def send_poll(update: Update, context: CallbackContext, index):
    if index < len(polls):
        poll = polls[index]
        keyboard = [
            [InlineKeyboardButton(opt, callback_data=opt)] for opt in poll["options"]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.callback_query:
            update.callback_query.edit_message_text(
                text=poll["question"], reply_markup=reply_markup
            )
        else:
            update.message.reply_text(poll["question"], reply_markup=reply_markup)
    else:
        update.callback_query.message.reply_text("✅ So‘rovnoma tugadi! Rahmat!")


# 🎯 Javobni qayta ishlash
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    index = context.user_data.get("poll_index", 0)

    user_answers[user_id][polls[index]["question"]] = query.data
    context.user_data["poll_index"] = index + 1

    if index + 1 < len(polls):
        send_poll(update, context, index + 1)
    else:
        query.edit_message_text("✅ So‘rovnoma yakunlandi! Rahmat!")


# 📊 /results — faqat admin uchun
def results(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        update.message.reply_text("⛔ Sizda bu buyruqdan foydalanish huquqi yo‘q.")
        return

    if not user_answers:
        update.message.reply_text("Hozircha javoblar yo‘q.")
        return

    text = "📊 <b>So‘rovnoma natijalari:</b>\n\n"
    for uid, answers in user_answers.items():
        text += f"👤 <b>{uid}</b>:\n"
        for q, a in answers.items():
            text += f"• {q} — <b>{a}</b>\n"
        text += "\n"

    update.message.reply_text(text, parse_mode="HTML")


# 🔧 Asosiy funksiya
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("results", results))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 Bot ishga tushdi...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
