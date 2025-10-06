# 1139713731  
# 8328899370:AAH8ZYttJKUzhEL6IFl9ipZBAqKiSx4JaRU
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext

ADMIN_ID = 1139713731  # Adminga o'zgartiring

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
        keyboard = [
            [
                InlineKeyboardButton("✅ Ha", callback_data="Ha"),
                InlineKeyboardButton("❌ Yo‘q", callback_data="Yo‘q")
            ],
            [
                InlineKeyboardButton("🤔 Hali bilmayman", callback_data="Hali bilmayman"),
                InlineKeyboardButton("📝 Boshqa", callback_data="Boshqa")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=chat_id,
            text="Bot sizga yoqmoqdami?",
            reply_markup=reply_markup
        )

    else:
        context.bot.send_message(chat_id=ADMIN_ID, text=f"Yangi talab/taklif:\n\n{text}")
        context.bot.send_message(chat_id=chat_id, text="Xabaringiz uchun rahmat!")

# Tugma bosilganda ishlovchi funksiya
def button_click(update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    answer = query.data

    # Foydalanuvchiga alert ko‘rsatish
    query.answer(
        text="Sizning javobingiz qabul qilindi! 😊",
        show_alert=True
    )

    # Adminga xabar yuborish
    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Foydalanuvchi {user.first_name} ({user.id}) quyidagi javobni tanladi: {answer}"
    )

# Main
def main():
    updater = Updater("8328899370:AAH8ZYttJKUzhEL6IFl9ipZBAqKiSx4JaRU", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    print("✅ Bot alertli versiyada ishlayapti...")
    updater.idle()

if __name__ == '__main__':
    main()
