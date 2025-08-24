from handlers import start,handleMessage
from config import BOT_TOKEN
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)

def main():
    updater = Updater(BOT_TOKEN, use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handleMessage))
    
    updater.start_polling()
    updater.idle()
    
if __name__ == "__main__" : main()