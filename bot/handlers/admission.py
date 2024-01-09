import json
from functools import partial

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, filters, CallbackContext, CommandHandler

from bot.utils.utils import get_keyboard, get_inline_keyboard, go_home, BACK, HOME

ADMISSION, BACHELOR, MASTER = range(3)


def json_to_dict(file_name: str) -> dict:
    with open(file_name, "r", encoding="UTF-8") as file:
        return json.load(file)


async def admission(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Бакалаврат')],
        [KeyboardButton(text='Магістратура')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Оберіть категорію:', reply_markup=reply_markup)
    return ADMISSION


async def bachelor(update: Update,
                   context: CallbackContext) -> int:
    faculties = json_to_dict("bot/utils/specialties.json")['Бакалаврат']
    # print("History Information:", faculties.keys())
    reply_markup = get_keyboard(faculties.keys(), back_button=True)
    await update.message.reply_text('Оберіть факультет:', reply_markup=reply_markup)
    return BACHELOR


async def master(update: Update, context: CallbackContext) -> int:
    pass


async def speciality(update: Update, context: CallbackContext, faculty: str) -> None:
    await update.message.reply_text(f' heheheasodij\'alksg: {faculty}')


admission_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Вступ на навчання'), admission)],
    states={
        ADMISSION: [
            MessageHandler(filters.Regex('Бакалаврат'), bachelor),
            MessageHandler(filters.Regex('Магістратура'), master),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        BACHELOR: [
            MessageHandler(filters.Regex(faculty), partial(speciality, faculty=faculty)) for
            faculty in json_to_dict("bot/utils/specialties.json")['Бакалаврат'].keys()
        ],
        MASTER: [
            MessageHandler(filters.Regex(faculty), partial(speciality, faculty=faculty)) for
            faculty in json_to_dict("bot/utils/specialties.json")['Магістратура'].keys()
        ]
    },
    fallbacks=[CommandHandler('start', admission)],
    name="admission-handler",
    persistent=True,
)
