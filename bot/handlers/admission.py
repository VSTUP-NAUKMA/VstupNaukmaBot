from functools import partial

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, filters, CallbackContext, CommandHandler

from bot.utils.utils import get_column_keyboard, go_home, BACK, HOME, json_to_dict

ADMISSION, BACHELOR, MASTER, SPECIALITY, QUESTIONS, ANSWER = range(6)

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
    context.user_data['degree'] = update.message.text
    reply_markup = get_column_keyboard(bachelor_faculties.keys(), back_button=True)
    await update.message.reply_text('Оберіть факультет:', reply_markup=reply_markup)
    return BACHELOR


async def master(update: Update, context: CallbackContext) -> int:
    context.user_data['degree'] = update.message.text
    reply_markup = get_column_keyboard(master_faculties.keys(), back_button=True)
    await update.message.reply_text('Оберіть факультет:', reply_markup=reply_markup)
    return MASTER


async def specialities(update: Update, context: CallbackContext) -> int:
    context.user_data['faculty'] = update.message.text

    degree = context.user_data.get('degree')
    faculty = context.user_data.get('faculty')

    print(f"{degree} : {faculty}")

    if degree:
        if degree == 'Бакалаврат' and faculty in bachelor_faculties:
            all_specialities = [name for value in bachelor_faculties[faculty].values() for name in value.keys()]
        elif degree == 'Магістратура' and faculty in master_faculties:
            all_specialities = [name for value in master_faculties[faculty].values() for name in value.keys()]
        else:
            return ConversationHandler.END

        reply_markup = get_column_keyboard(all_specialities, back_button=True)
        await update.message.reply_text('Оберіть спеціальність:', reply_markup=reply_markup)
        return SPECIALITY

    return ConversationHandler.END


async def questions(update: Update, context: CallbackContext) -> int:
    context.user_data['speciality'] = update.message.text
    reply_markup = get_column_keyboard(questions_list, back_button=True)
    await update.message.reply_text(f'Оберіть спеціальність: ', reply_markup=reply_markup)
    return QUESTIONS


async def answer(update: Update, context: CallbackContext) -> int:
    context.user_data['question'] = update.message.text

    degree = context.user_data.get('degree')
    faculty = context.user_data.get('faculty')
    speciality = context.user_data.get('speciality')
    question = context.user_data.get('question')

    all_specialities = [value for value in bachelor_faculties[faculty].values()]
    answers = {key1: value1 for small_dict in all_specialities for key1, value1 in small_dict.items()}

    if speciality in answers and question in answers[speciality]:
        print(answers[speciality][question])
    else:
        print(
            f"Answer not found for degree '{degree}' faculty '{faculty}' and speciality '{speciality}' and question '{question}'")

    reply_markup = get_column_keyboard([], back_button=True)
    await update.message.reply_text(f'{answers[speciality][question]}', reply_markup=reply_markup)
    return ANSWER


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
                MessageHandler(filters.Regex(faculty), specialities)
                for faculty in bachelor_faculties.keys()
            ],
            MessageHandler(filters.Regex(BACK), admission),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        MASTER: [
            *[
                MessageHandler(filters.Regex(faculty), specialities)
                for faculty in master_faculties.keys()
            ],
            MessageHandler(filters.Regex(BACK), admission),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        SPECIALITY: [
            MessageHandler(filters.Regex(BACK), admission),
            MessageHandler(filters.Regex(HOME), go_home),
            MessageHandler(filters.Regex('.*'), questions),
        ],
        QUESTIONS: [
            MessageHandler(filters.Regex(BACK), specialities),
            MessageHandler(filters.Regex(HOME), go_home),
            *[MessageHandler(filters.Regex(question), answer) for question in questions_list]
        ],
        ANSWER: [
            MessageHandler(filters.Regex(BACK), questions),
            MessageHandler(filters.Regex(HOME), go_home),
        ]

    },
    fallbacks=[CommandHandler('start', admission)],
    name="admission-handler",
    persistent=True,
)
