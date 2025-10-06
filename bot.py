# 1139713731  
# 8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4
import os
import csv
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PollAnswerHandler, CallbackContext

# Environment variables
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Poll tracking
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

# Xabarlarni ishlovchi funksiya
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
        context.bot.send_message(chat_id=ADMIN_ID, text=f"Yangi talab/taklif:\n\n{text}")
        context.bot.send_message(chat_id=chat_id, text="Xabaringiz uchun rahmat!")
        start(update, context)

# Poll javoblarini CSV va adminga yuborish
def handle_poll_answer(update, context: CallbackContext):
    poll_answer = update.poll_answer
    chat_id = update.effective_chat.id
    user_id = poll_answer.user.id
    poll_id = poll_answer.poll_id
    answers = poll_answer.option_ids

    # CSV saqlash
    with open("results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, poll_id, answers])

    # Adminga real vaqt yuborish
    context.bot.send_message(chat_id=ADMIN_ID, text=f"Foydalanuvchi {user_id} so'rovnomaga javob berdi: {answers}")

    # Foydalanuvchiga xabar, agar barcha poll javoblari berilgan bo‘lsa
    if chat_id in active_polls:
        if poll_id in active_polls[chat_id]:
            active_polls[chat_id].remove(poll_id)
        if not active_polls[chat_id]:
            # Hammasi to‘ldirilgan
            context.bot.send_message(chat_id=user_id, text="Surovnomada ishtirok etganingiz uchun rahmat! ✅")
            start(update, context)  # Bosh menyuga qaytarish
            del active_polls[chat_id]  # Tozalash

# Main
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(PollAnswerHandler(handle_poll_answer))

    updater.start_polling()
    print("Bot ishga tushdi...")
    updater.idle()

if __name__ == "__main__":
    main()
