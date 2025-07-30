import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from http import HTTPStatus

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Your verb list (keep your existing 500 verbs here)
verbs = [
    {"id": 1, "italian": "andare", "english": "to go"},
    {"id": 2, "italian": "promettere", "english": "to promise"}
]

# For Vercel, we need to persist state differently since it's serverless
# Using a simple dictionary (not ideal for production)
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
        user_progress[chat_id] = 0  # Reset progress

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

# Vercel-specific handler
async def handler(request):
    if request.method == "POST":
        # Initialize application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("restart", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
        
        # Process update
        try:
            data = await request.json()
            update = Update.de_json(data, application.bot)
            await application.process_update(update)
            return {"statusCode": HTTPStatus.OK}
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            return {"statusCode": HTTPStatus.INTERNAL_SERVER_ERROR}
    
    return {"statusCode": HTTPStatus.OK, "body": "Bot is running"}

# For local testing
if __name__ == "__main__":
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("restart", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
    application.run_polling()