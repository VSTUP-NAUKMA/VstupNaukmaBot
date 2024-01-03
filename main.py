import asyncio
import os

import logging

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler

from bot.config import load_env
from bot.handlers.operator_chat import reply_handler, button_callback, clear_pending_replies
from bot.handlers.start import conv_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

if __name__ == '__main__':
    load_env()
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    button_handler = CallbackQueryHandler(button_callback)
    application.add_handler(button_handler)
    application.add_handler(conv_handler)
    application.add_handler(reply_handler)
    loop = asyncio.get_event_loop()
    loop.create_task(clear_pending_replies(86400))  # 24 hours
    application.run_polling(allowed_updates=Update.ALL_TYPES)
