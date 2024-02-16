from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

from bot.handlers.contacts import go_home
from bot.utils.fields import *
from bot.utils.utils import generic_reply

BACK = 'Назад'
HOME = 'На головну'
PROCESS, OPPORTUNITIES, FEATURES, DIFFERENCE, FEATURES_LAST_CHOICE, OPPORTUNITIES_LAST_CHOICE, DIFFERENCE_LAST_CHOICE, PROGRAMS, CAMPUS, PROGRAMS_LAST_CHOICE, CAMPUS_LAST_CHOICE = range(
    11)


async def process(update: Update, context: CallbackContext) -> int:
    buttons = [
        ['Особливості навчання в НаУКМА', 'Можливості'],
        ['Різниця між університетом та школою', 'Сертифікатні програми'],
        ['Кампус'],
    ]
    return await generic_reply(update, 'Оберіть категорію:', buttons, PROCESS, back_button=True)


async def opportunities(update: Update, context: CallbackContext) -> int:
    buttons = [['Мобільність', 'Працевлаштування'],
               ['Навчальна практика']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, OPPORTUNITIES, back_button=True, home_button=True)


async def features(update: Update, context: CallbackContext) -> int:
    buttons = [['Триместри', 'Індивідуальний навчальний план'],
               ['Організація навчання', 'Оцінювання викладачів'], ['Вибіркові дисципліни', 'Формат навчання'],
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
    return await generic_reply(update, TRIMESTER_TEXT, [], DIFFERENCE_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def grade_system(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, TRIMESTER_TEXT, [], DIFFERENCE_LAST_CHOICE, back_button=True, home_button=True,
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
    return await generic_reply(update, TRIMESTER_TEXT, [], FEATURES_LAST_CHOICE, back_button=True, home_button=True,
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
                               back_home_row=True)


async def practice(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, PRACTICE_TEXT, [], OPPORTUNITIES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def work(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, WORK_TEXT, [], OPPORTUNITIES_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def bachelor(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, WORK_TEXT, [], PROGRAMS_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def master(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, WORK_TEXT, [], PROGRAMS_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def buildings(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, WORK_TEXT, [], CAMPUS_LAST_CHOICE, back_button=True, home_button=True,
                               back_home_row=True)


async def chill_zones(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, WORK_TEXT, [], CAMPUS_LAST_CHOICE, back_button=True, home_button=True,
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
            MessageHandler(filters.Regex(BACK), go_home),
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
    fallbacks=[],
    name='study_process-handler',
    persistent=True,
)
