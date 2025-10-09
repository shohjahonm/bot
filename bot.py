# 1139713731   969555465
# 8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4
import os
import csv
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PollAnswerHandler, CallbackContext

# TOKEN va ADMIN_ID ni bu yerga yoz
TOKEN = "8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4"
ADMIN_ID = 1139713731

# So‘rovnomalarni kuzatish uchun
active_polls = {}  # chat_id: list of poll_ids


# /start komandasi
def start(update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("📨 Talab va takliflar"), KeyboardButton("📊 So‘rovnomada qatnashish")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Assalomu alaykum! 👋\nAristocrat Cafe botiga xush kelibsiz!\nQuyidagi menyudan birini tanlang:",
        reply_markup=reply_markup
    )


# Oddiy xabarlarni ishlovchi funksiya
def handle_message(update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == "📨 Talab va takliflar":
        context.bot.send_message(chat_id=chat_id, text="Iltimos, talab yoki taklifingizni yozing:")

    elif text == "📊 So‘rovnomada qatnashish":
        questions = [
            "Bot sizga yoqmoqdami?",
            "Xizmat darajasi sizni qoniqtirdimi?",
            "Taomlar sifati qanday?"
        ]
        options = ["Ha", "Yo‘q", "Hali bilmayman", "Boshqa"]
        poll_ids = []
        for q in questions:
            poll_message = context.bot.send_poll(
                chat_id=chat_id,
                question=q,
                options=options,
                is_anonymous=False,
                allows_multiple_answers=True
            )
            poll_ids.append(poll_message.poll.id)
        active_polls[chat_id] = poll_ids

    else:
        # Talab/taklif yuborilganida
        context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Yangi talab/taklif:\n\n{text}")
        context.bot.send_message(chat_id=chat_id, text="Xabaringiz uchun rahmat! ✅")
        start(update, context)


# Poll javoblarini CSV faylga yozish va adminga yuborish
def handle_poll_answer(update, context: CallbackContext):
    poll_answer = update.poll_answer
    user_id = poll_answer.user.id
    poll_id = poll_answer.poll_id
    answers = poll_answer.option_ids

    # Chatni poll_id orqali topamiz
    chat_id = None
    for c_id, polls in active_polls.items():
        if poll_id in polls:
            chat_id = c_id
            break

    # Natijani CSV faylga yozish
    with open("results.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, chat_id, poll_id, answers])

    # Adminga yuborish
    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🗳 Foydalanuvchi {user_id} so‘rovnomaga javob berdi: {answers}"
    )

    # Agar barcha poll to‘ldirilgan bo‘lsa
    if chat_id and chat_id in active_polls:
        if poll_id in active_polls[chat_id]:
            active_polls[chat_id].remove(poll_id)
        if not active_polls[chat_id]:
            context.bot.send_message(chat_id=chat_id, text="Surovnomada ishtirok etganingiz uchun rahmat! ✅")
            start(update, context)
            del active_polls[chat_id]


# /result komandasi — barcha natijalarni olish
def show_results(update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id != ADMIN_ID:
        update.message.reply_text("⛔ Bu buyruq faqat admin uchun!")
        return

    if os.path.exists("results.csv"):
        with open("results.csv", "r", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        if not rows:
            update.message.reply_text("Hali hech kim so‘rovnomani to‘ldirmagan 😕")
            return

        text = "📊 So‘rovnoma natijalari:\n\n"
        for row in rows:
            user_id, chat_id_r, poll_id, answers = row
            text += f"👤 Foydalanuvchi: {user_id}\n🗳 Poll ID: {poll_id}\n✅ Javob: {answers}\n\n"

        if len(text) > 4000:
            with open("results.csv", "rb") as f:
                context.bot.send_document(chat_id=chat_id, document=f)
        else:
            update.message.reply_text(text)
    else:
        update.message.reply_text("Natijalar fayli topilmadi 😕")


# Asosiy funksiya
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("result", show_results))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(PollAnswerHandler(handle_poll_answer))

    updater.start_polling()
    print("✅ Bot ishga tushdi...")
    updater.idle()


if __name__ == "__main__":
    main()
