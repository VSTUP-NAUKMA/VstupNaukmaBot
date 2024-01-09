import os

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

BACK = 'Назад'
HOME = 'На головну'


def get_keyboard(*row_buttons, back_button=False):
    keyboard = [list(map(KeyboardButton, row)) for row in row_buttons]
    if back_button:
        keyboard.append([KeyboardButton(BACK)])
        keyboard.append([KeyboardButton(HOME)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_inline_keyboard(*row_buttons, back_button=False):
    keyboard = [list(map(lambda btn: InlineKeyboardButton(btn, callback_data=btn.lower()), row)) for row in row_buttons]
    if back_button:
        keyboard.append([InlineKeyboardButton("Back", callback_data='back')])
        keyboard.append([InlineKeyboardButton("Home", callback_data='home')])
    return InlineKeyboardMarkup(keyboard)


async def go_home(update: Update, context: CallbackContext) -> int:
    from bot.handlers.start import start
    await start(update, context)
    return ConversationHandler.END


def delete_persistence_file():
    if os.path.exists("bot.pickle"):
        os.remove("bot.pickle")
