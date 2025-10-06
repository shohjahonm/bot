# 1139713731  
# 8328899370:AAH8ZYttJKUzhEL6IFl9ipZBAqKiSx4JaRU
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext

ADMIN_ID = 1139713731  # o'zingizning Telegram ID'ingiz

# Foydalanuvchi tanlovlarini saqlash uchun
user_votes = {}

OPTIONS = ["Ha", "Yo‘q", "Hali bilmayman", "Boshqa"]

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
        send_poll_menu(chat_id, context)

    else:
        context.bot.send_message(chat_id=ADMIN_ID, text=f"Yangi talab/taklif:\n\n{text}")
        context.bot.send_message(chat_id=chat_id, text="Xabaringiz uchun rahmat!")

# So‘rovnoma menyusini yuborish
def send_poll_menu(chat_id, context):
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"vote_{opt}")] for opt in OPTIONS
    ]
    keyboard.append([InlineKeyboardButton("✅ Yuborish", callback_data="submit_votes")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=chat_id,
        text="Bot sizga yoqmoqdami? Bir nechta variantni tanlang (bosganda belgi qo‘yiladi):",
        reply_markup=reply_markup
    )

# Tugma bosilganda ishlovchi funksiya
def button_click(update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data.startswith("vote_"):
        option = data.replace("vote_", "")

        # Foydalanuvchi tanlovlarini saqlash
        if user_id not in user_votes:
            user_votes[user_id] = set()

        if option in user_votes[user_id]:
            user_votes[user_id].remove(option)
        else:
            user_votes[user_id].add(option)

        # Keyboardni yangilash (tanlanganlarga ✅ qo‘yish)
        keyboard = []
        for opt in OPTIONS:
            text = f"✅ {opt}" if opt in user_votes[user_id] else opt
            keyboard.append([InlineKeyboardButton(text, callback_data=f"vote_{opt}")])
        keyboard.append([InlineKeyboardButton("✅ Yuborish", callback_data="submit_votes")])

        query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))

    elif data == "submit_votes":
        votes = user_votes.get(user_id, set())
        if not votes:
            query.answer("Hech narsa tanlanmadi 😅", show_alert=True)
            return

        # Alert bilan rahmat xabari
        query.answer("Javoblaringiz qabul qilindi! 😊", show_alert=True)

        # Adminga yuborish
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Foydalanuvchi {query.from_user.first_name} ({user_id}) quyidagi variantlarni tanladi:\n" +
                 ", ".join(votes)
        )

        # Statistikani yangilash va ko‘rsatish
        show_results(context, query)

# Natijalarni ko‘rsatish
def show_results(context, query):
    # Hisoblash
    stats = {opt: 0 for opt in OPTIONS}
    for votes in user_votes.values():
        for v in votes:
            if v in stats:
                stats[v] += 1

    total = sum(stats.values())
    if total == 0:
        total = 1

    result_text = "📊 <b>Hozirgi natijalar:</b>\n\n"
    for opt, count in stats.items():
        percent = (count / total) * 100
        result_text += f"{opt}: {count} ta ({percent:.1f}%)\n"

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=result_text,
        parse_mode="HTML"
    )

# Main
def main():
    updater = Updater(" 8328899370:AAH8ZYttJKUzhEL6IFl9ipZBAqKiSx4JaRU", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    print("✅ Bot multiple select va natija ko‘rsatish rejimida ishlayapti...")
    updater.idle()

if __name__ == '__main__':
    main()
