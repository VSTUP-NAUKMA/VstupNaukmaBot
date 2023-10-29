import os

from telegram import Update
from telegram.ext import Application

from bot.config import load_env
from bot.handlers.operator_chat import reply_handler
from bot.handlers.start import conv_handler

if __name__ == '__main__':
    load_env()
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    application.add_handler(conv_handler)
    application.add_handler(reply_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
