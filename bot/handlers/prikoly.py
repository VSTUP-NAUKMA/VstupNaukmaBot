import os
import random

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters, CommandHandler

from bot.handlers.start import fresh_start
from bot.utils.utils import unlucky

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


load_images("bot/photos/prikoly")


async def get_random_image():
    if not IMAGE_PATHS:
        return "Files not found in directory"
    return random.choice(IMAGE_PATHS)


REPLY_KEYBOARD = [['Спеціальності Академії', 'Система вступу'],
                  ['Студентське життя', 'Навчальний процес'],
                  ['Контакти', 'Гуртожитки'],
                  ['Чат-підтримка', 'Хочу приколюху 😜']]

KEYBOARD_MARKUP = ReplyKeyboardMarkup(REPLY_KEYBOARD, resize_keyboard=True)


async def send_meme(update: Update, context: CallbackContext) -> int:
    TELEGRAM_SUPPORT_CHAT_ID = os.getenv('TELEGRAM_SUPPORT_CHAT_ID')
    chat_id = update.message.chat_id
    if int(chat_id) == int(TELEGRAM_SUPPORT_CHAT_ID):
        return
    user = update.message.from_user
    username = user.username
    await update.message.reply_photo(await get_random_image(), reply_markup=KEYBOARD_MARKUP)
    if username == 'malashokk':
        await update.message.reply_text("Наташа хватить", reply_markup=KEYBOARD_MARKUP)


prikoly_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Хочу приколюху 😜'), send_meme)],
    states={},
    fallbacks=[CommandHandler('reset', fresh_start), MessageHandler(filters.TEXT, unlucky)],
    name='prikoly-handler',
    persistent=True,
)
