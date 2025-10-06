# 1139713731  
# 8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4
from telegram import Update, Poll
from telegram.ext import ApplicationBuilder, CommandHandler, PollHandler, ContextTypes
import json
import os

# TOKEN va ADMIN_ID ni o'zingizga qarab yozing
TOKEN = "8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4"
ADMIN_ID = 1139713731
DATA_FILE = "poll_results.json"


# /start — so‘rovnoma yuborish
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Bot sizga yoqmoqdami?"
    options = ["Ha", "Yo‘q", "Hali bilmayman", "Boshqa"]
    msg = await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=question,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )

    # pollni keyinchalik natijalar uchun saqlaymiz
    context.bot_data[msg.poll.id] = {"question": question, "options": options}


# Poll javoblarini saqlash
async def poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user = answer.user
    selected = answer.option_ids

    # poll haqida ma'lumot olish
    poll_info = context.bot_data.get(answer.poll_id)
    if not poll_info:
        return

    question = poll_info["question"]
    options = poll_info["options"]
    selected_answers = [options[i] for i in selected]

    # mavjud ma'lumotni o‘qish
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[str(user.id)] = {
        "username": user.username or user.full_name,
        "answers": selected_answers
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    # foydalanuvchiga rahmat
    await context.bot.send_message(chat_id=user.id, text="✅ So‘rovnomada ishtirok etganingiz uchun rahmat!")


# Admin uchun natijalarni chiqarish
async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Siz admin emassiz.")
        return

    if not os.path.exists(DATA_FILE):
        await update.message.reply_text("📭 Hali hech kim javob bermagan.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if not data:
        await update.message.reply_text("📭 Hali javob yo‘q.")
        return

    text = "📊 *So‘rovnoma natijalari:*\n\n"
    for uid, info in data.items():
        username = info["username"]
        text += f"👤 {username}:\n"
        for ans in info["answers"]:
            text += f"   • {ans}\n"
        text += "\n"

    await update.message.reply_text(text, parse_mode="Markdown")


# Main — botni ishga tushurish
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(PollHandler(poll_answer))
    app.add_handler(CommandHandler("results", results))

    print("✅ Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
