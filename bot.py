# 1139713731  
# 8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4
import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext

# TOKENni Heroku Config Vars dan olish
TOKEN = os.getenv("8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4")

ADMIN_ID = 1139713731  # o'zingizni ID
user_votes = {}  # foydalanuvchi tanlovlari
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

# Inline so‘rovnoma yuborish
def send_poll_menu(chat_id, context):
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"vote_{opt}")] for opt in OPTIONS]
    keyboard.append([InlineKeyboardButton("✅ Yuborish", callback_data="submit_votes")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=chat_id,
        text="Bot sizga yoqmoqdami? Bir nechta variantni tanlang:",
        reply_markup=reply_markup
    )

# Tugmalarni qayta ishlash
def button_click(update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data.startswith("vote_"):
        option = data.replace("vote_", "")
        if user_id not in user_votes:
            user_votes[user_id] = set()

        # Tanlash/tanlamaslikni almashtiramiz
        if option in user_votes[user_id]:
            user_votes[user_id].remove(option)
        else:
            user_votes[user_id].add(option)

        # Klaviaturani yangilaymiz
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

        query.answer("Javoblaringiz qabul qilindi! 😊", show_alert=True)

        # Adminga yuborish
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🧑‍💻 Foydalanuvchi {query.from_user.first_name} ({user_id}) tanlagan variantlar:\n{', '.join(votes)}"
        )

        # Natijalarni ko‘rsatish
        show_results(context, query)

# /natijalar komandasi (faqat admin uchun)
def show_results_command(update, context):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("Bu buyruq faqat admin uchun!")
        return

    result_text = get_results_text()
    update.message.reply_text(result_text, parse_mode="HTML")

# Natijalarni hisoblash
def get_results_text():
    stats = {opt: 0 for opt in OPTIONS}
    for votes in user_votes.values():
        for v in votes:
            if v in stats:
                stats[v] += 1

    total = sum(stats.values()) or 1

    result_text = "📊 <b>Umumiy natijalar:</b>\n\n"
    for opt, count in stats.items():
        percent = (count / total) * 100
        bars = "▮" * int(percent // 10) + "▯" * (10 - int(percent // 10))
        result_text += f"{opt}: {count} ta ({percent:.1f}%)\n{bars}\n\n"
    return result_text

# Foydalanuvchiga natijani ko‘rsatish
def show_results(context, query):
    result_text = get_results_text()
    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=result_text,
        parse_mode="HTML"
    )

# Main
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("natijalar", show_results_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    print("✅ Bot ishlayapti...")
    updater.idle()

if __name__ == '__main__':
    main()
