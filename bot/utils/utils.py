import json
import os

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.handlers.start import home

BACK = 'Назад'
HOME = 'На головну'


def create_keyboard_button(text):
    return KeyboardButton(text)


def get_keyboard(rows, add_back_button=False, add_home_button=False, is_final_method=False):
    keyboard = [[create_keyboard_button(button) for button in row] for row in rows]
    if add_back_button or add_home_button:
        back_home_row = []
        if add_back_button:
            back_home_row.append(create_keyboard_button(BACK))
        if add_home_button:
            back_home_row.append(create_keyboard_button(HOME))
        if is_final_method:
            keyboard.append(back_home_row)
        else:
            if add_back_button:
                keyboard.append([create_keyboard_button(BACK)])
            if add_home_button:
                keyboard.append([create_keyboard_button(HOME)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def generic_reply(update, text, buttons, state, image_path=None, back_button=False, home_button=False,
                        back_home_row=False,
                        parse_mode=None):
    reply_markup = get_keyboard(buttons, add_back_button=back_button, add_home_button=home_button,
                                is_final_method=back_home_row)
    if parse_mode:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode,
                                        disable_web_page_preview=True)
    elif image_path:
        await update.message.reply_text(text, reply_markup=reply_markup)
        await update.message.reply_photo(photo=image_path, reply_markup=reply_markup)

    else:
        await update.message.reply_text(text, reply_markup=reply_markup)
    return state


async def go_home(update: Update, context: CallbackContext) -> int:
    await home(update, context)
    return ConversationHandler.END


def delete_persistence_file():
    if os.path.exists("bot.pickle"):
        os.remove("bot.pickle")


def json_to_dict(file_name: str) -> dict:
    with open(file_name, "r", encoding="UTF-8") as file:
        return json.load(file)


def save_chat_id(chat_id):
    with open("registered_chat_ids.txt", "a") as file:
        file.write(str(chat_id) + "\n")


def is_chat_id_registered(chat_id):
    with open("registered_chat_ids.txt", "r") as file:
        for line in file:
            if str(chat_id) == line.strip():
                return True
    return False


async def unlucky(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("""Я тебе не розумію :(
Використовуй клавіатуру знизу для комунікації зі мною""")
