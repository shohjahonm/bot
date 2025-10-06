
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Admin ID ni kiritish
ADMIN_ID = 1139713731  # admin ID

# Stage identifiers for conversation
TALAB_TAKLIF, FEEDBACK = range(2)

# Start command handler
def start(update: Update, context):
    keyboard = [
        [KeyboardButton('Talab va Takliflar')],
        [KeyboardButton('Surovnomada Ishtirok Etish')],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Salom! Talab va Takliflar yoki Surovnomada Ishtirok Etish uchun birini tanlang.", reply_markup=reply_markup)
    return TALAB_TAKLIF

# Handle the "Talab va Takliflar" button press
def talab_taklif(update: Update, context):
    update.message.reply_text("Iltimos, talab yoki taklifingizni yozing:")
    return FEEDBACK

# Handle the "Surovnomada Ishtirok Etish" button press
def surovnomada_ishtirok(update: Update, context):
    update.message.reply_text("Siz surovnomada ishtirok etasiz. Iltimos, javobni yozing.")
    return FEEDBACK

# Capture the user's feedback and send a thank you message
def feedback(update: Update, context):
    user_feedback = update.message.text
    # Here you can process the feedback, save it, etc.
    update.message.reply_text(f"Fikrlaringiz uchun rahmat! Sizning fikringiz: {user_feedback}")
    
    # Admin uchun feedback yuborish
    context.bot.send_message(chat_id=ADMIN_ID, text=f"Yangi fikr: {user_feedback}")
    
    return ConversationHandler.END

# Define the main function to set up the conversation handler
def main():
    # Replace 'YOUR_BOT_TOKEN' with your bot's token
    updater = Updater("8328899370:AAH8ZYttJKUzhEL6IFl9ipZBAqKiSx4JaRU", use_context=True)
    dp = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TALAB_TAKLIF: [
                MessageHandler(Filters.regex('^Talab va Takliflar$'), talab_taklif),
                MessageHandler(Filters.regex('^Surovnomada Ishtirok Etish$'), surovnomada_ishtirok),
            ],
            FEEDBACK: [MessageHandler(Filters.text & ~Filters.command, feedback)],
        },
        fallbacks=[],
    )

    dp.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
