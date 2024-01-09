from functools import partial

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, filters, CallbackContext, CommandHandler

from bot.utils.utils import get_column_keyboard, go_home, BACK, HOME, json_to_dict

ADMISSION, BACHELOR, MASTER, SPECIALITY, QUESTIONS = range(5)

bachelor_faculties = json_to_dict("bot/utils/specialties.json")['Бакалаврат']
master_faculties = json_to_dict("bot/utils/specialties.json")['Магістратура']
questions_list = ['Загальна інформація', 'Дисципліни', 'НМТ', 'Вартість',
                  'Кількість місць', 'Коефіцієнти', 'Прохідний бал',
                  'Сайт спеціальності', 'Сайт конкурс']


async def admission(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Бакалаврат')],
        [KeyboardButton(text='Магістратура')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Оберіть категорію:', reply_markup=reply_markup)
    return ADMISSION


async def bachelor(update: Update, context: CallbackContext) -> int:
    reply_markup = get_column_keyboard(bachelor_faculties.keys(), back_button=True)
    await update.message.reply_text('Оберіть факультет:', reply_markup=reply_markup)
    return BACHELOR


async def master(update: Update, context: CallbackContext) -> int:
    reply_markup = get_column_keyboard(master_faculties.keys(), back_button=True)
    await update.message.reply_text('Оберіть факультет:', reply_markup=reply_markup)
    return MASTER


async def speciality(update: Update, context: CallbackContext, speciality_set: dict) -> int:
    print(type(questions_list))
    all_specialities = [name for key, value in speciality_set.items() for name in value.keys()]
    reply_markup = get_column_keyboard(all_specialities, back_button=True)
    await update.message.reply_text(f'Оберіть спеціальність: ', reply_markup=reply_markup)
    return SPECIALITY


async def questions(update: Update, context: CallbackContext) -> int:
    reply_markup = get_column_keyboard(questions_list, back_button=True)
    await update.message.reply_text(f'Що вас цікавить: ', reply_markup=reply_markup)
    return QUESTIONS


admission_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Вступ на навчання'), admission)],
    states={
        ADMISSION: [
            MessageHandler(filters.Regex('Бакалаврат'), bachelor),
            MessageHandler(filters.Regex('Магістратура'), master),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        BACHELOR: [
            *[
                MessageHandler(filters.Regex(faculty), partial(speciality, speciality_set=bachelor_faculties[faculty]))
                for faculty in bachelor_faculties.keys()
            ],
            MessageHandler(filters.Regex(BACK), admission),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        MASTER: [
            *[
                MessageHandler(filters.Regex(faculty), partial(speciality, speciality_set=master_faculties[faculty]))
                for faculty in master_faculties.keys()
            ],
            MessageHandler(filters.Regex(BACK), admission),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        SPECIALITY: [
            *[
                MessageHandler(filters.Regex(question), questions) for question in questions_list
            ],
            MessageHandler(filters.Regex(BACK), admission),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        QUESTIONS: [

        ]

    },
    fallbacks=[CommandHandler('start', admission)],
    name="admission-handler",
    persistent=True,
)
