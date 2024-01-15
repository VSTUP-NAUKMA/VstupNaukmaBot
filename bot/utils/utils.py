import os
import json

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


def get_column_keyboard(*column_buttons, back_button=False):
    keyboard = [[KeyboardButton(text=button)] for button in list(column_buttons[0])]
    # print(column_buttons)
    if back_button:
        keyboard.append([KeyboardButton(BACK)])
        keyboard.append([KeyboardButton(HOME)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def go_home(update: Update, context: CallbackContext) -> int:
    from bot.handlers.start import start
    await start(update, context)
    return ConversationHandler.END


def delete_persistence_file():
    if os.path.exists("bot.pickle"):
        os.remove("bot.pickle")


def json_to_dict(file_name: str) -> dict:
    with open(file_name, "r", encoding="UTF-8") as file:
        return json.load(file)
