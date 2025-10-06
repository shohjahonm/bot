from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Admin ID — o'zingizni telegram ID'ingizni yozing
ADMIN_ID = 1139713731  # O'ZGARTIRING

# /start komandasi
def start(update, context):
    keyboard = [
        [KeyboardButton("📨 Talab va takliflar"), KeyboardButton("📊 So‘rovnomada qatnashish")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Quyidagi menyudan birini tanlang:", reply_markup=reply_markup)

# Xabarlarni ishlovchi funksiya
def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == "📨 Talab va takliflar":
        context.bot.send_message(chat_id=chat_id, text="Iltimos, talab yoki taklifingizni yozing:")

    elif text == "📊 So‘rovnomada qatnashish":
        context.bot.send_poll(
            chat_id=chat_id,
            question="Bot sizga yoqmoqdami?",
            options=["Ha", "Yoq", "Hali bilmayman"],
            is_anonymous=False
        )

    else:
        context.bot.send_message(chat_id=ADMIN_ID, text=f"Yangi talab/taklif:\n\n{text}")
        context.bot.send_message(chat_id=chat_id, text="Xabaringiz uchun rahmat!")

# Main
def main():
    updater = Updater("BOT_TOKEN", use_context=True)  # BOT_TOKEN ni almashtiring

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    print("Bot ishlayapti...")
    updater.idle()

if __name__ == '__main__':
    main()
