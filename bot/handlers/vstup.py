from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters, CommandHandler

from bot.handlers.start import fresh_start
from bot.utils.fields import *
from bot.utils.utils import generic_reply, go_home, unlucky

BACK = 'Назад'
HOME = 'На головну'
VSTUP, SELECT_LEVEL, ENTRY_DESCRIPTION_NEXT, ENTRY_DESCRIPTION_END, ENTRY_DATES_NEXT, ENTRY_EXAM_NEXT, ENTRY_EXAM_END, APPLICANT_CABINET_NEXT, APPLICANT_CABINET_END, VSTUP_END, ENTRY_DATES_END = range(
    11)

CATEGORY_BUTTONS = {
    'education': [['Бакалаврат', 'Магістратура']],
    'entry_master': [
        ['Опис системи вступу', 'Дати вступної кампанії'],
        ['Документи для вступу', 'Електронний кабінет вступника'],
        ['Мотиваційний лист', 'Вступні іспити']
    ],
    'entry_bachelor': [
        ['Опис системи вступу', 'Дати вступної кампанії'],
        ['Документи для вступу', 'Електронний кабінет вступника'],
        ['Мотиваційний лист']
    ],
    'exam': [
        ['ЄВІ', 'ЄФВВ'],
        ['Фаховий іспит', 'Реєстрація'],
        ['Дати проведення']
    ],
    'cabinet': [['Реєстрація', 'Подача заявок']],
    'bachelor': [['Бюджет', 'Контракт']],
    'master': [['На основі бакалаврату', 'На основі магістратури']]

}
CATEGORY_BUTTONS_REGEX = {key: '|'.join([btn for sublist in val for btn in sublist])
                          for key, val in CATEGORY_BUTTONS.items()}


async def select_level(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Оберіть категорію:', CATEGORY_BUTTONS['education'], SELECT_LEVEL,
                               back_button=True)


async def set_education_level(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    context.user_data['level'] = user_choice
    return await vstup_system(update, context)


async def vstup_system(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('level') == 'Бакалаврат':
        buttons_new = CATEGORY_BUTTONS['entry_bachelor']
    else:
        buttons_new = CATEGORY_BUTTONS['entry_master']
    return await generic_reply(update, 'Оберіть категорію:', buttons_new, VSTUP, back_button=True, home_button=True)


async def entry_description(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('level') == 'Бакалаврат':
        text = 'Оберіть форму навчання:'
        buttons = CATEGORY_BUTTONS['bachelor']
    else:
        text = 'Оберіть основу для вступу:'
        buttons = CATEGORY_BUTTONS['master']
    return await generic_reply(update, text, buttons, ENTRY_DESCRIPTION_NEXT, back_button=True, home_button=True)


async def description_end(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('level') == 'Бакалаврат':
        match update.message.text:
            case 'Бюджет':
                text = BACHELOR_BUDGET_DESCRIPTION_TEXT
                return await generic_reply(update, text, [], ENTRY_DESCRIPTION_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)
            case 'Контракт':
                text = BACHELOR_CONTRACT_DESCRIPTION_TEXT
                return await generic_reply(update, text, [], ENTRY_DESCRIPTION_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)
    else:
        match update.message.text:
            case 'На основі бакалаврату':
                text = APPLICATIONS_MASTER_ON_BACHELOR
                return await generic_reply(update, text, [], ENTRY_DESCRIPTION_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)
            case 'На основі магістратури':
                text = APPLICATIONS_MASTER_ON_MASTER
                return await generic_reply(update, text, [], ENTRY_DESCRIPTION_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def entry_dates(update: Update, context: CallbackContext) -> int:
    text = 'Оберіть форму навчання:'
    buttons = CATEGORY_BUTTONS['bachelor']
    return await generic_reply(update, text, buttons, ENTRY_DATES_NEXT, back_button=True, home_button=True)


async def entry_dates_end(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('level') == 'Бакалаврат':
        match update.message.text:
            case 'Бюджет':
                text = DATES_BACHELOR_BUDGET_TEXT
                return await generic_reply(update, text, [], ENTRY_DATES_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)
            case 'Контракт':
                text = DATES_BACHELOR_CONTRACT_TEXT
                return await generic_reply(update, text, [], ENTRY_DATES_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)
    else:
        match update.message.text:
            case 'Бюджет':
                text = DATES_MASTER_BUDGET_TEXT
                return await generic_reply(update, text, [], ENTRY_DATES_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)
            case 'Контракт':
                text = DATES_MASTER_CONTRACT_TEXT
                return await generic_reply(update, text, [], ENTRY_DATES_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def entry_exams(update: Update, context: CallbackContext) -> int:
    text = 'Оберіть категорію:'
    return await generic_reply(update, text, CATEGORY_BUTTONS['exam'], ENTRY_EXAM_NEXT, back_button=True,
                               home_button=True)


async def entry_exams_end(update: Update, context: CallbackContext) -> int:
    match update.message.text:
        case 'ЄВІ':
            text = MASTER_EVI
            return await generic_reply(update, text, [], ENTRY_EXAM_END, back_button=True, home_button=True,
                                       back_home_row=True, parse_mode=ParseMode.MARKDOWN)
        case 'ЄФВВ':
            text = MASTER_EFVV
            return await generic_reply(update, text, [], ENTRY_EXAM_END, back_button=True, home_button=True,
                                       back_home_row=True, parse_mode=ParseMode.MARKDOWN)
        case 'Фаховий іспит':
            text = MASTER_EXAM
            return await generic_reply(update, text, [], ENTRY_EXAM_END, back_button=True, home_button=True,
                                       back_home_row=True, parse_mode=ParseMode.MARKDOWN)
        case 'Реєстрація':
            text = MASTER_REGISTRATION
            return await generic_reply(update, text, [], ENTRY_EXAM_END, back_button=True, home_button=True,
                                       back_home_row=True)
        case 'Дати проведення':
            text = DATES_MASTER_TEXT
            return await generic_reply(update, text, [], ENTRY_EXAM_END, back_button=True, home_button=True,
                                       back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def applicant_cabinet(update: Update, context: CallbackContext) -> int:
    text = 'Оберіть категорію:'
    buttons = CATEGORY_BUTTONS['cabinet']
    return await generic_reply(update, text, buttons, APPLICANT_CABINET_NEXT, back_button=True,
                               home_button=True, parse_mode=ParseMode.MARKDOWN)


async def applicant_cabinet_end(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('level') == 'Бакалаврат':
        match update.message.text:
            case 'Реєстрація':
                text = BACHELOR_CABINET_TEXT
                return await generic_reply(update, text, [], APPLICANT_CABINET_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)
            case 'Подача заявок':
                text = APPLICATIONS_BACHELOR_TEXT
                return await generic_reply(update, text, [], APPLICANT_CABINET_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)
    else:
        match update.message.text:
            case 'Реєстрація':
                text = MASTER_CABINET_TEXT
                return await generic_reply(update, text, [], APPLICANT_CABINET_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)
            case 'Подача заявок':
                text = APPLICATIONS_MASTER_TEXT
                return await generic_reply(update, text, [], APPLICANT_CABINET_END, back_button=True, home_button=True,
                                           back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def motivational_letter(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('level') == 'Бакалаврат':
        text = MOTIVATION_BACHELOR_TEXT
    else:
        text = MOTIVATION_MASTER_TEXT
    return await generic_reply(update, text, [], VSTUP_END, back_button=True, home_button=True,
                               back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def entry_documents(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('level') == 'Бакалаврат':
        text = BACHELOR_DOCUMENTS_TEXT
    else:
        text = MASTER_DOCUMENTS_TEXT
    return await generic_reply(update, text, [], VSTUP_END, back_button=True, home_button=True,
                               back_home_row=True, parse_mode=ParseMode.MARKDOWN)


vstup_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Система вступу'), select_level)],
    states={
        SELECT_LEVEL: [
            MessageHandler(filters.Regex('Бакалаврат|Магістратура'), set_education_level),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        VSTUP: [
            MessageHandler(filters.Regex('Опис системи вступу'), entry_description),
            MessageHandler(filters.Regex('Дати вступної кампанії'), entry_dates),
            MessageHandler(filters.Regex('Вступні іспити'), entry_exams),
            MessageHandler(filters.Regex('Електронний кабінет вступника'), applicant_cabinet),
            MessageHandler(filters.Regex('Мотиваційний лист'), motivational_letter),
            MessageHandler(filters.Regex('Документи для вступу'), entry_documents),
            MessageHandler(filters.Regex(BACK), select_level),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        ENTRY_EXAM_NEXT: [
            MessageHandler(filters.Regex(CATEGORY_BUTTONS_REGEX['exam']), entry_exams_end),
            MessageHandler(filters.Regex(BACK), vstup_system),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        ENTRY_EXAM_END: [
            MessageHandler(filters.Regex(BACK), entry_exams),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        ENTRY_DESCRIPTION_NEXT: [
            MessageHandler(filters.Regex(CATEGORY_BUTTONS_REGEX['bachelor'] + '|' + CATEGORY_BUTTONS_REGEX['master']),
                           description_end),
            MessageHandler(filters.Regex(BACK), vstup_system),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        ENTRY_DESCRIPTION_END: [
            MessageHandler(filters.Regex(BACK), entry_description),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        ENTRY_DATES_NEXT: [
            MessageHandler(filters.Regex(CATEGORY_BUTTONS_REGEX['bachelor']), entry_dates_end),
            MessageHandler(filters.Regex(BACK), vstup_system),
            MessageHandler(filters.Regex(HOME), go_home),

        ],
        ENTRY_DATES_END: [
            MessageHandler(filters.Regex(BACK), entry_dates),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        APPLICANT_CABINET_NEXT: [
            MessageHandler(filters.Regex(CATEGORY_BUTTONS_REGEX['cabinet']), applicant_cabinet_end),
            MessageHandler(filters.Regex(BACK), vstup_system),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        APPLICANT_CABINET_END: [
            MessageHandler(filters.Regex(BACK), applicant_cabinet),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        VSTUP_END: [
            MessageHandler(filters.Regex(BACK), vstup_system),
            MessageHandler(filters.Regex(HOME), go_home),
        ]
    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start),
               MessageHandler(filters.TEXT, unlucky)],
    name='vstup_handler',
    persistent=True,
)
