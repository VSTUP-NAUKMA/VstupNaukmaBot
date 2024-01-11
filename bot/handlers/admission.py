from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, filters, CallbackContext, CommandHandler

from bot.utils.utils import get_column_keyboard, go_home, BACK, HOME, json_to_dict

ADMISSION, FACULTY, SPECIALITY, QUESTION, ANSWER = range(5)

warehouse = json_to_dict("bot/utils/specialties.json")


async def admission(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Бакалаврат')],
        [KeyboardButton(text='Магістратура')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Оберіть категорію:', reply_markup=reply_markup)

    return ADMISSION


async def faculty(update: Update, context: CallbackContext) -> int:
    if update.message.text != BACK:
        context.user_data['degree'] = update.message.text
    # print(f"faculty function : degree {context.user_data.get('degree')}")
    # print(warehouse[context.user_data.get('degree')].keys())
    reply_markup = get_column_keyboard(warehouse
                                       [context.user_data.get('degree')].keys(),
                                       back_button=True)
    await update.message.reply_text('Оберіть факультет:', reply_markup=reply_markup)
    return FACULTY


async def speciality(update: Update, context: CallbackContext) -> int:
    if update.message.text != BACK:
        context.user_data['faculty'] = update.message.text
    # print(f"speciality function : faculty {context.user_data.get('faculty')}")
    # print(warehouse[context.user_data.get('degree')][context.user_data.get('faculty')].keys())
    reply_markup = get_column_keyboard(warehouse
                                       [context.user_data.get('degree')]
                                       [context.user_data.get('faculty')].keys(),
                                       back_button=True)
    await update.message.reply_text('Оберіть спеціальність:', reply_markup=reply_markup)
    return SPECIALITY


async def question(update: Update, context: CallbackContext) -> int:
    if update.message.text != BACK:
        context.user_data['speciality'] = update.message.text
    # print(f"question function : speciality{context.user_data.get('speciality')}")
    # print(warehouse[context.user_data.get('degree')][context.user_data.get('faculty')].keys())
    reply_markup = get_column_keyboard(warehouse
                                       [context.user_data.get('degree')]
                                       [context.user_data.get('faculty')]
                                       [context.user_data.get('speciality')].keys(),
                                       back_button=True)
    await update.message.reply_text('Оберіть питання:', reply_markup=reply_markup)
    return QUESTION


async def answer(update: Update, context: CallbackContext) -> int:
    if update.message.text != BACK:
        context.user_data['question'] = update.message.text
    # print(f"answer function : question {context.user_data.get('question')}")
    # print(warehouse[context.user_data.get('degree')][context.user_data.get('faculty')].keys())
    reply_markup = get_column_keyboard([], back_button=True)
    await update.message.reply_text(
        f"{warehouse[context.user_data.get('degree')][context.user_data.get('faculty')][context.user_data.get('speciality')][context.user_data.get('question')]}",
        reply_markup=reply_markup)
    return ANSWER


admission_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Вступ на навчання'), admission)],
    states={
        ADMISSION: [
            MessageHandler(filters.Regex('Бакалаврат'), faculty),
            MessageHandler(filters.Regex('Магістратура'), faculty),
            MessageHandler(filters.Regex(BACK), go_home)
        ],
        FACULTY: [
            MessageHandler(filters.Regex(BACK), admission),
            MessageHandler(filters.Regex(HOME), go_home),
            MessageHandler(filters.Regex('.*'), speciality)
        ],
        SPECIALITY: [
            MessageHandler(filters.Regex(BACK), faculty),
            MessageHandler(filters.Regex(HOME), go_home),
            MessageHandler(filters.Regex('.*'), question)
        ],
        QUESTION: [
            MessageHandler(filters.Regex(BACK), speciality),
            MessageHandler(filters.Regex(HOME), go_home),
            MessageHandler(filters.Regex('.*'), answer)
        ],
        ANSWER: [
            MessageHandler(filters.Regex(BACK), question),
            MessageHandler(filters.Regex(HOME), go_home),
        ]

    },
    fallbacks=[CommandHandler('start', admission)],
    name="admission-handler",
    persistent=True,
)
