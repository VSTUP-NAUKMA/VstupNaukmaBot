from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, filters, CommandHandler, CallbackQueryHandler

from bot.utils.utils import *

ADMISSION, FACULTY, SPECIALITY, QUESTION, ANSWER, CALCULATE = range(6)

warehouse = json_to_dict("bot/utils/specialties.json")


async def admission(update: Update, context: CallbackContext) -> int:
    buttons = [['Бакалаврат', 'Магістратура']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, ADMISSION, back_button=True)


async def faculty(update: Update, context: CallbackContext) -> int:
    if update.message.text != BACK:
        context.user_data['degree'] = update.message.text
    buttons = list(map(lambda x: [x], warehouse[context.user_data.get('degree')].keys()))
    return await generic_reply(update, 'Оберіть факультет:', buttons, FACULTY, back_button=True)


async def clear_scores(context: CallbackContext):
    keys_to_clear = ['score_Українска мова', 'score_Математика', 'score_Історія України', 'score_bonus']
    for key in keys_to_clear:
        context.user_data.pop(key, None)


async def speciality(update: Update, context: CallbackContext) -> int:
    if update.message.text != BACK:
        context.user_data['faculty'] = update.message.text
    buttons = list(
        map(lambda x: [x], warehouse[context.user_data.get('degree')][context.user_data.get('faculty')].keys()))
    return await generic_reply(update, 'Оберіть спеціальність:', buttons, SPECIALITY, back_button=True)


async def question(update: Update, context: CallbackContext) -> int:
    if update.message.text == BACK:
        await clear_scores(context)
    else:
        context.user_data['speciality'] = update.message.text
    buttons = list(map(lambda x: [x], warehouse[context.user_data.get('degree')][context.user_data.get('faculty')][
        context.user_data.get('speciality')].keys()))
    return await generic_reply(update, 'Оберіть питання:', buttons, QUESTION, back_button=True)


async def answer(update: Update, context: CallbackContext) -> int:
    if update.message.text != BACK:
        context.user_data['question'] = update.message.text
    answer_reply = \
        warehouse[context.user_data.get('degree')][context.user_data.get('faculty')][
            context.user_data.get('speciality')][
            context.user_data.get('question')]
    return await generic_reply(update, f"{answer_reply}", [], ANSWER, back_button=True)


async def calculate(update: Update, context: CallbackContext) -> int:
    if update.message.text != BACK:
        context.user_data['question'] = update.message.text
    answer_reply = \
        warehouse[context.user_data.get('degree')][context.user_data.get('faculty')][
            context.user_data.get('speciality')][
            context.user_data.get('question')]
    keyboard = [

        [InlineKeyboardButton("Українська мова", callback_data="Українська мова")],
        [InlineKeyboardButton("Математика", callback_data="Математика")],
        [InlineKeyboardButton("Історія України", callback_data="Історія України")],
        [InlineKeyboardButton("Додатково", callback_data="bonus")],

    ]

    context.user_data['coefficients'] = answer_reply
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Оберіть бали", reply_markup=reply_markup)
    return CALCULATE


async def enter_score(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    selected_subject = query.data  # 'ukr', 'math', 'hist', 'extra'

    # Збережіть вибраний предмет у контексті для подальшого використання
    context.user_data['selected_subject'] = selected_subject

    await query.edit_message_text(text=f"Введіть ваш бал з {selected_subject}:")
    return CALCULATE


async def score_received(update: Update, context: CallbackContext) -> int:
    user_score = float(update.message.text)
    selected_subject = context.user_data['selected_subject']

    coefficients_list = context.user_data['coefficients'].split()

    # Розрахунок остаточного балу
    subject_index = {"Українська мова": 0, "Математика": 1, "Історія України": 2, "extra": 3}
    coefficient = float(coefficients_list[subject_index[selected_subject]])

    final_score = user_score * coefficient
    context.user_data[f'score_{selected_subject}'] = str(user_score) + "*" + str(coefficient) + " = " + str(final_score)


    # Оновлення інлайн-клавіатури
    keyboard = [
        [InlineKeyboardButton(f"Українська мова: {context.user_data.get('score_Українська мова', '')}",
                              callback_data="Українська мова")],
        [InlineKeyboardButton(f"Математика: {context.user_data.get('score_Математика', '')}",
                              callback_data="Математика")],
        [InlineKeyboardButton(f"Історія України: {context.user_data.get('score_Історія України', '')}",
                              callback_data="Історія України")],
        [InlineKeyboardButton(f"Додатково: {context.user_data.get('score_bonus', 'Додатково')}", callback_data="bonus")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text="Виберіть наступний предмет або завершіть введення балів.",
        reply_markup=reply_markup
    )

    return CALCULATE


admission_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Вступ на навчання'), admission)],
    states={
        ADMISSION: [MessageHandler(filters.Regex('Бакалаврат|Магістратура'), faculty),
                    MessageHandler(filters.Regex(BACK), go_home)],
        FACULTY: [MessageHandler(filters.Regex(BACK), admission),
                  MessageHandler(filters.Regex(HOME), go_home), MessageHandler(filters.Regex('.*'), speciality)],
        SPECIALITY: [MessageHandler(filters.Regex(BACK), faculty),
                     MessageHandler(filters.Regex(HOME), go_home), MessageHandler(filters.Regex('.*'), question)],
        QUESTION: [MessageHandler(filters.Regex('Розрахувати бали'), calculate),
                   MessageHandler(filters.Regex(BACK), speciality),
                   MessageHandler(filters.Regex(HOME), go_home), MessageHandler(filters.Regex('.*'), answer)],
        CALCULATE: [
            CallbackQueryHandler(enter_score, pattern='^(Історія України|Математика|Українська мова|bonus)$'),
            MessageHandler(filters.Regex(BACK), question),
            MessageHandler(filters.Regex(HOME), go_home),
            MessageHandler(filters.TEXT & ~filters.COMMAND, score_received)
        ],
        ANSWER: [
            MessageHandler(filters.Regex(BACK), question), MessageHandler(filters.Regex(HOME), go_home)]
    },
    fallbacks=[CommandHandler('start', admission)],
    name="admission-handler",
    persistent=True,
)
