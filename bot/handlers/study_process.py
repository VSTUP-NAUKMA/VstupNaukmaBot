import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters, CommandHandler

from bot.handlers.contacts import go_home
from bot.handlers.start import fresh_start
from bot.utils.fields import *
from bot.utils.utils import generic_reply, unlucky

BACK = 'Назад'
HOME = 'На головну'
PROCESS, OPPORTUNITIES, FEATURES, DIFFERENCE, FEATURES_LAST_CHOICE, OPPORTUNITIES_LAST_CHOICE, DIFFERENCE_LAST_CHOICE, PROGRAMS, CAMPUS, PROGRAMS_LAST_CHOICE, CAMPUS_LAST_CHOICE = range(
    11)


async def process(update: Update, context: CallbackContext) -> int:
    TELEGRAM_SUPPORT_CHAT_ID = os.getenv('TELEGRAM_SUPPORT_CHAT_ID')
    chat_id = update.message.chat_id
    if int(chat_id) == int(TELEGRAM_SUPPORT_CHAT_ID):
        return
    buttons = [
        ['Особливості навчання в НаУКМА', 'Сертифікатні програми'],
        ['Кампус', 'Можливості'],
        ['Різниця між університетом та школою'],
    ]
    return await generic_reply(update, 'Оберіть категорію:', buttons, PROCESS, back_button=True)


async def opportunities(update: Update, context: CallbackContext) -> int:
    buttons = [['Мобільність', 'Працевлаштування'],
               ['Навчальна практика']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, OPPORTUNITIES, back_button=True, home_button=True)


async def features(update: Update, context: CallbackContext) -> int:
    buttons = [['Триместри', 'Організація навчання'],
               ['Індивідуальний навчальний план', 'Оцінювання викладачів'], ['Вибіркові дисципліни', 'Формат навчання'],
               ['Розклад']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, FEATURES, back_button=True, home_button=True)


async def difference(update: Update, context: CallbackContext) -> int:
    buttons = [['Різниця в термінах', 'Система оцінювання']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, DIFFERENCE, back_button=True, home_button=True)


async def programs(update: Update, context: CallbackContext) -> int:
    buttons = [['Бакалаврат', 'Магістратура']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, PROGRAMS, back_button=True, home_button=True)


async def campus(update: Update, context: CallbackContext) -> int:
    buttons = [['Корпуси', 'Де поїсти/відпочити біля КМА']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, CAMPUS, back_button=True, home_button=True)


async def term_difference(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, DIFFERENCE_TEXT, [], DIFFERENCE_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def grade_system(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, GRADE_SYSTEM, [], DIFFERENCE_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def trimesters(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, TRIMESTER_TEXT, [], FEATURES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def inp(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, INP_TEXT, [], FEATURES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def organization(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, ORGANIZATION_TEXT, [], FEATURES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def teachers(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, TEACHER_TEXT, [], FEATURES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def disciplines(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, DISCIPLINES_TEXT, [], FEATURES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def study_format(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, STUDY_FORMAT, [], FEATURES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def schedule(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, SCHEDULE_TEXT, [], FEATURES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def mobility(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, MOBILITY_TEXT, [], OPPORTUNITIES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def practice(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, PRACTICE_TEXT, [], OPPORTUNITIES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def work(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, WORK_TEXT, [], OPPORTUNITIES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def bachelor(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, SERT_BACHELOR, [], PROGRAMS_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def master(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, SERT_MASTER, [], PROGRAMS_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def buildings(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, BUILDINGS_TEXT, [], CAMPUS_LAST_CHOICE,'bot/photos/2024-06-03 17.15.55.jpg', back_button=True, home_button=True,
                               back_home_row=True)


async def chill_zones(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, CHILL_TEXT, [], CAMPUS_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


# Структура ConversationHandler
study_process_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Навчальний процес'), process)],
    states={
        PROCESS: [
            MessageHandler(filters.Regex('Особливості навчання в НаУКМА'), features),
            MessageHandler(filters.Regex('Можливості'), opportunities),
            MessageHandler(filters.Regex('Різниця між університетом та школою'), difference),
            MessageHandler(filters.Regex('Сертифікатні програми'), programs),
            MessageHandler(filters.Regex('Кампус'), campus),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        OPPORTUNITIES: [
            MessageHandler(filters.Regex('Мобільність'), mobility),
            MessageHandler(filters.Regex('Працевлаштування'), work),
            MessageHandler(filters.Regex('Навчальна практика'), practice),
            MessageHandler(filters.Regex(BACK), process),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        FEATURES: [
            MessageHandler(filters.Regex('Триместри'), trimesters),
            MessageHandler(filters.Regex('Індивідуальний навчальний план'), inp),
            MessageHandler(filters.Regex('Організація навчання'), organization),
            MessageHandler(filters.Regex('Оцінювання викладачів'), teachers),
            MessageHandler(filters.Regex('Вибіркові дисципліни'), disciplines),
            MessageHandler(filters.Regex('Формат навчання'), study_format),
            MessageHandler(filters.Regex('Розклад'), schedule),
            MessageHandler(filters.Regex(BACK), process),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        DIFFERENCE: [
            MessageHandler(filters.Regex('Різниця в термінах'), term_difference),
            MessageHandler(filters.Regex('Система оцінювання'), grade_system),
            MessageHandler(filters.Regex(BACK), process),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        PROGRAMS: [
            MessageHandler(filters.Regex('Бакалаврат'), bachelor),
            MessageHandler(filters.Regex('Магістратура'), master),
            MessageHandler(filters.Regex(BACK), process),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        CAMPUS: [
            MessageHandler(filters.Regex('Корпуси'), buildings),
            MessageHandler(filters.Regex('Де поїсти/відпочити біля КМА'), chill_zones),
            MessageHandler(filters.Regex(BACK), process),
            MessageHandler(filters.Regex(HOME), go_home),
        ],

        FEATURES_LAST_CHOICE: [
            MessageHandler(filters.Regex(BACK), features),
            MessageHandler(filters.Regex(HOME), go_home),
        ],

        OPPORTUNITIES_LAST_CHOICE: [
            MessageHandler(filters.Regex(BACK), opportunities),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        DIFFERENCE_LAST_CHOICE: [
            MessageHandler(filters.Regex(BACK), difference),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        PROGRAMS_LAST_CHOICE: [
            MessageHandler(filters.Regex(BACK), programs),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        CAMPUS_LAST_CHOICE: [
            MessageHandler(filters.Regex(BACK), campus),
            MessageHandler(filters.Regex(HOME), go_home),
        ]

    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start), MessageHandler(filters.TEXT, unlucky)],
    name='study_process-handler',
    persistent=True,
)
