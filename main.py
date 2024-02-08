import asyncio
import logging
import os
import atexit

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, PicklePersistence

from bot.handlers.contacts import contacts_handler
from bot.handlers.dormitory import dormitory_handler
from bot.handlers.operator_chat import reply_handler, button_callback, clear_pending_replies, operator_chat_handler
from bot.handlers.start import start_handler
from bot.handlers.admission import admission_handler
from bot.handlers.student_life import student_life_handler
from bot.handlers.study_process import study_process_handler
from bot.utils.config import load_env

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
if __name__ == '__main__':
    load_env()
    persistence = PicklePersistence(filepath="bot.pickle")
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).persistence(
        persistence=persistence).concurrent_updates(True).build()
    button_handler = CallbackQueryHandler(button_callback)
    application.add_handler(start_handler)
    application.add_handler(operator_chat_handler)
    application.add_handler(dormitory_handler)
    application.add_handler(admission_handler)
    application.add_handler(student_life_handler)
    application.add_handler(contacts_handler)
    application.add_handler(study_process_handler)

    application.add_handler(button_handler)
    application.add_handler(reply_handler)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(clear_pending_replies(86400))  # 24 hours
    application.run_polling(allowed_updates=Update.ALL_TYPES)
