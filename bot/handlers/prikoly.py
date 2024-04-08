import os
import random

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

IMAGE_PATHS = []


def load_images(directory):
    global IMAGE_PATHS
    if not os.path.exists(directory):
        print("Directory not found")
        return

    IMAGE_PATHS = [os.path.join(directory, f) for f in os.listdir(directory) if
                   os.path.isfile(os.path.join(directory, f))]
    if not IMAGE_PATHS:
        print("No files found in directory")


load_images("bot/photos")


def get_random_image():
    if not IMAGE_PATHS:
        return "Files not found in directory"
    return random.choice(IMAGE_PATHS)


REPLY_KEYBOARD = [['Вступ на навчання', 'Система вступу'],
                  ['Студентське життя', 'Навчальний процес'],
                  ['Контакти', 'Гуртожитки'],
                  ['Чат-підтримка', 'Хочу приколюху 😜']]
KEYBOARD_MARKUP = ReplyKeyboardMarkup(REPLY_KEYBOARD, resize_keyboard=True)


async def send_meme(update: Update, context: CallbackContext) -> int:
    await update.message.reply_photo(get_random_image(), reply_markup=KEYBOARD_MARKUP)


prikoly_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Хочу приколюху 😜'), send_meme)],
    states={

    },
    fallbacks=[],
    name='prikoly-handler',
    persistent=True,
)
