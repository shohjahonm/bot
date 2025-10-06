# 1139713731  
# 8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4
import os
import json
from telegram import Update, Poll
from telegram.ext import ApplicationBuilder, CommandHandler, PollHandler, ContextTypes

TOKEN = os.getenv("8328899370:AAFatemiB1503HFYFzauBWLsgtQCu2X1MB4")
ADMIN_ID = 1139713731  # bu yerga o'zingizning Telegram ID yozing
DATA_FILE = "poll_results.json"


# --- Poll yaratish ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Sizga qaysi texnologiyalar yoqadi?"
    options = ["Python", "JavaScript", "C++", "Java", "Rust", "Go"]
    await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=question,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )


# --- Poll javoblarini saqlash ---
async def poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user_id = answer.user.id
    username = answer.user.username or answer.user.full_name
    selected_options = answer.option_ids

    # poll natijalarini olish
    poll_message = context.bot_data.get(answer.poll_id)
    if not poll_message:
        return

    question = poll_message["question"]
    options = poll_message["options"]

    # foydalanuvchi tanlagan variantlar
    selected_texts = [options[i] for i in selected_options]

    # mavjud faylni o'qish
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[str(user_id)] = {
        "username": username,
        "answers": selected_texts
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# --- Poll yuborilganini saqlash ---
async def poll_created(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poll = update.poll
    context.bot_data[poll.id] = {"question": poll.question, "options": poll.options}


# --- Admin uchun barcha natijalarni chiqarish ---
async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Siz admin emassiz.")
        return

    if not os.path.exists(DATA_FILE):
        await update.message.reply_text("Hali hech kim javob bermagan.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if not data:
        await update.message.reply_text("Hali javob yo‘q.")
        return

    text = "📊 *Poll natijalari:*\n\n"
    for user, info in data.items():
        text += f"👤 @{info['username'] if info['username'] else user}:\n"
        for ans in info["answers"]:
            text += f"   • {ans}\n"
        text += "\n"

    await update.message.reply_text(text, parse_mode="Markdown")


# --- Main ---
def main():
    if not TOKEN:
        raise ValueError("TOKEN yo‘q! Heroku config vars’da TOKEN o‘rnatilganini tekshiring.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(PollHandler(poll_created))
    app.add_handler(CommandHandler("results", results))
    app.add_handler(PollHandler(poll_answer))

    print("✅ Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
