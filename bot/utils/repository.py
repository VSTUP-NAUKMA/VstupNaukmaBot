from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

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


async def generic_reply(update, text, buttons, state, back_button=False, home_button=False, back_home_row=False):
    reply_markup = get_keyboard(buttons, add_back_button=back_button, add_home_button=home_button,
                                is_final_method=back_home_row)
    await update.message.reply_text(text, reply_markup=reply_markup)
    return state


async def go_home(update: Update, context: CallbackContext) -> int:
    from bot.handlers.start import start
    await start(update, context)
    return ConversationHandler.END
