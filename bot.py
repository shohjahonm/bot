# 1139713731  
# 8328899370:AAH8ZYttJKUzhEL6IFl9ipZBAqKiSx4JaRU

from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PollAnswerHandler

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
            is_anonymous=False,
            allows_multiple_answers=True
        )

    else:
        # Talab yoki taklif yuborilganida adminga yuborish va foydalanuvchiga "Raxmat" xabarini yuborish
        context.bot.send_message(chat_id=ADMIN_ID, text=f"Yangi talab/taklif:\n\n{text}")
        context.bot.send_message(chat_id=chat_id, text="Xabaringiz uchun rahmat!")

# So'rovnoma tugagandan keyin raxmat aytish
def handle_poll_answer(update, context: CallbackContext):
    poll_answer = update.poll_answer
    chat_id = update.effective_chat.id

    # So'rovnomada javob yuborilganda
    context.bot.send_message(chat_id=chat_id, text="Surovnomada ishtirok etganingiz uchun rahmat!")

    # Adminga javoblar haqida ma'lumot yuborish
    answer_text = "\n".join(poll_answer.option_ids)
    context.bot.send_message(chat_id=ADMIN_ID, text=f"Foydalanuvchi so'rovnomaga javob berdi:\n{answer_text}")

# So'rovnomani tugatish
def handle_poll_end(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Surovnoma yakunlandi. Ishtirok etganingiz uchun rahmat!")

# Main
def main():
    updater = Updater("8328899370:AAH8ZYttJKUzhEL6IFl9ipZBAqKiSx4JaRU", use_context=True)  # BOT_TOKEN ni almashtiring
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(PollAnswerHandler(handle_poll_answer))  # So'rovnoma tugagandan keyin raxmat yuborish

    updater.start_polling()
    print("Bot ishlayapti...")
    updater.idle()

if __name__ == '__main__':
    main()
