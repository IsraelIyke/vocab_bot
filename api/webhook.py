import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Store token from environment or fallback (not recommended for production)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8279668033:AAGE9Mg9k20tQVXRHCzY1eVhVDlojvKuNic")

# Verb list
verbs = [
    {"id": 1, "italian": "andare", "english": "to go"},
    {"id": 2, "italian": "avere", "english": "to have"},
    {"id": 500, "italian": "promettere", "english": "to promise"}
]

# Store user progress
user_progress = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_progress[chat_id] = 0
    await ask_question(update, context)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    current_index = user_progress.get(chat_id, 0)
    if current_index < len(verbs):
        verb = verbs[current_index]
        await update.message.reply_text(
            f"({verb['id']}/{len(verbs)}) What does **{verb['italian']}** mean?"
        )
    else:
        await update.message.reply_text("🎉 Congratulations! You've completed all 500 verbs!")
        user_progress[chat_id] = 0

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    current_index = user_progress.get(chat_id, 0)
    if current_index < len(verbs):
        verb = verbs[current_index]
        user_answer = update.message.text.lower().strip()
        correct_answer = verb['english'].lower()

        if user_answer == correct_answer:
            response = f"✅ Correct! **{verb['italian']}** means **{verb['english']}**."
        else:
            response = f"❌ Not quite. **{verb['italian']}** means **{verb['english']}**."

        await update.message.reply_text(response)
        user_progress[chat_id] = current_index + 1
        await ask_question(update, context)

async def webhook(request):
    """Vercel webhook handler."""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("restart", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    if request.method == "POST":
        data = await request.json()
        await application.update_queue.put(Update.de_json(data, application.bot))
        return {"statusCode": 200, "body": "ok"}
    else:
        return {"statusCode": 200, "body": "Bot is running"}

# Required for Vercel
handler = webhook
