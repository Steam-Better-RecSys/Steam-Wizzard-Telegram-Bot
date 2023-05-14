import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

url = "https://api.steamwizzard.com/health"
interval_mins = 1


async def check_api(context: ContextTypes.DEFAULT_TYPE):
    res = requests.get(url)
    try:
        json = res.json()
    except:
        await context.bot.send_message(chat_id=context.job.chat_id, text="❌ DOWN")
    else:
        if json["status"] == "up":
            await context.bot.send_message(chat_id=context.job.chat_id, text="✅ OK")
        else:
            await context.bot.send_message(
                chat_id=context.job.chat_id, text="⚠️ STRANGE"
            )


async def start_auto_messaging(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    await context.bot.send_message(chat_id, text="🏁Start watching...")
    context.job_queue.run_repeating(
        check_api, interval=interval_mins * 60, data=name, chat_id=chat_id
    )


if __name__ == "__main__":
    load_dotenv()
    app = ApplicationBuilder().token(os.getenv("API_KEY")).build()
    app.add_handler(CommandHandler("notify", start_auto_messaging))
    app.run_polling()
