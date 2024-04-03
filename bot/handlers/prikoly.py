import os
import random

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters


def get_random_image(directory):
    if not os.path.exists(directory):
        return "Директорія не знайдена"

    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if not files:
        return "Файли не знайдені у директорії"

    return random.choice(files)





async def send_meme(update: Update, context: CallbackContext) -> int:

    reply_keyboard = [['Вступ на навчання', 'Система вступу'],
                      ['Студентське життя', 'Навчальний процес'],
                      ['Контакти', 'Гуртожитки'],
                      ['Чат-підтримка', 'Хочу приколюху 😜']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_photo(get_random_image("bot/photos1"), reply_markup=keyboard_markup)

prikoly_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Хочу приколюху 😜'), send_meme)],
    states={

    },
    fallbacks=[],
    name='prikoly-handler',
    persistent=True,
)
