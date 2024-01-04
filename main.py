import asyncio
import logging
import os

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler

from bot.handlers.operator_chat import reply_handler, button_callback, clear_pending_replies, conv_handler
from bot.handlers.start import start_handler, dormitory_handler
from bot.utils.config import load_env

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

if __name__ == '__main__':
    load_env()
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    button_handler = CallbackQueryHandler(button_callback)
    application.add_handler(start_handler)
    application.add_handler(conv_handler)
    application.add_handler(dormitory_handler)

    # Інші хендлери, такі як button_handler, reply_handler і т.д.
    application.add_handler(button_handler)
    application.add_handler(reply_handler)

    loop = asyncio.get_event_loop()
    loop.create_task(clear_pending_replies(86400))  # 24 hours
    application.run_polling(allowed_updates=Update.ALL_TYPES)
