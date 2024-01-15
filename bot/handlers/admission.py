from telegram.ext import MessageHandler, filters, CommandHandler

from bot.utils.utils import *

ADMISSION, FACULTY, SPECIALITY, QUESTION, ANSWER = range(5)

warehouse = json_to_dict("bot/utils/specialties.json")


async def admission(update: Update, context: CallbackContext) -> int:
    buttons = [['Бакалаврат', 'Магістратура']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, ADMISSION, back_button=True)


async def faculty(update: Update, context: CallbackContext) -> int:
    if update.message.text != BACK:
        context.user_data['degree'] = update.message.text
    buttons = list(map(lambda x: [x], warehouse[context.user_data.get('degree')].keys()))
    return await generic_reply(update, 'Оберіть факультет:', buttons, FACULTY, back_button=True)


async def speciality(update: Update, context: CallbackContext) -> int:
    print("speciality")
    if update.message.text != BACK:
        context.user_data['faculty'] = update.message.text
    buttons = list(
        map(lambda x: [x], warehouse[context.user_data.get('degree')][context.user_data.get('faculty')].keys()))
    return await generic_reply(update, 'Оберіть спеціальність:', buttons, SPECIALITY, back_button=True)


async def question(update: Update, context: CallbackContext) -> int:
    print("question")
    if update.message.text != BACK:
        context.user_data['speciality'] = update.message.text
    buttons = list(map(lambda x: [x], warehouse[context.user_data.get('degree')][context.user_data.get('faculty')][
        context.user_data.get('speciality')].keys()))
    return await generic_reply(update, 'Оберіть питання:', buttons, QUESTION, back_button=True)


async def answer(update: Update, context: CallbackContext) -> int:
    print("answer")
    if update.message.text != BACK:
        context.user_data['question'] = update.message.text
    answer_reply = \
        warehouse[context.user_data.get('degree')][context.user_data.get('faculty')][
            context.user_data.get('speciality')][
            context.user_data.get('question')]
    return await generic_reply(update, f"{answer_reply}", [], ANSWER, back_button=True)


admission_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Вступ на навчання'), admission)],
    states={
        ADMISSION: [MessageHandler(filters.Regex('Бакалаврат|Магістратура'), faculty),
                    MessageHandler(filters.Regex(BACK), go_home)],
        FACULTY: [MessageHandler(filters.Regex(BACK), admission),
                  MessageHandler(filters.Regex(HOME), go_home), MessageHandler(filters.Regex('.*'), speciality)],
        SPECIALITY: [MessageHandler(filters.Regex(BACK), faculty),
                     MessageHandler(filters.Regex(HOME), go_home), MessageHandler(filters.Regex('.*'), question)],
        QUESTION: [MessageHandler(filters.Regex(BACK), speciality),
                   MessageHandler(filters.Regex(HOME), go_home), MessageHandler(filters.Regex('.*'), answer)],
        ANSWER: [MessageHandler(filters.Regex(BACK), question), MessageHandler(filters.Regex(HOME), go_home)]
    },
    fallbacks=[CommandHandler('start', admission)],
    name="admission-handler",
    persistent=True,
)
