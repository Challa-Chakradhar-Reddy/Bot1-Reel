# from handlers import start, handleMessage
# from config import BOT_TOKEN
# import logging
# import os
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# # Better logging format
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# PORT = int(os.environ.get("PORT", 8443))  # Railway/Render will inject PORT

# def error_handler(update, context):
#     """Log Errors caused by Updates."""
#     logger.error(msg="Exception while handling an update:", exc_info=context.error)
#     if update and update.effective_message:
#         update.effective_message.reply_text("⚠️ Something went wrong. Please try again later.")

# def main():
#     updater = Updater(BOT_TOKEN, use_context=True)
#     dp = updater.dispatcher

#     # Handlers
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handleMessage))

#     # Error handler
#     dp.add_error_handler(error_handler)

#     # ---- Webhook Setup ----
#     app_url = os.getenv("APP_URL")  # e.g. "https://your-app-name.onrender.com"
#     if not app_url:
#         raise ValueError("❌ APP_URL not set in environment variables")

#     logger.info("🤖 Starting bot with webhook...")
#     updater.start_webhook(
#         listen="0.0.0.0",  # bind to all network interfaces
#         port=PORT,
#         url_path=BOT_TOKEN,
#         webhook_url=f"{app_url}/{BOT_TOKEN}"  # full webhook endpoint
#     )

#     updater.idle()

# if __name__ == "__main__":
#     main()


import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from handlers import start, handleMessage
from config import BOT_TOKEN

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Telegram Bot & Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, None, workers=0)

# Handlers
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handleMessage))

# Error handler
def error_handler(update, context):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and update.effective_message:
        update.effective_message.reply_text("⚠️ Something went wrong. Please try again later.")

dp.add_error_handler(error_handler)

# Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "ok", 200

# Health check root endpoint
@app.route("/", methods=["GET"])
def home():
    return "🤖 Bot is running on Railway!", 200


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8443))
    app.run(host="0.0.0.0", port=PORT)
