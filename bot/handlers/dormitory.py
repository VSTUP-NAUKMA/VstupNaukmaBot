from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, filters

from bot.utils.fields import *
from bot.utils.utils import generic_reply, go_home

BACK = 'Назад'
HOME = 'На головну'
DORMITORY, MASTERS, BACHELORS, ORDERS, PRICE, GURTO, DOCUMENT_REVIEW, VORZEL, ADVICE, ORDERS_NEXT = range(10)


async def dormitory(update: Update, context: CallbackContext) -> int:
    buttons = [['Для магістрів', 'Для бакалаврів'], ['Поселення', 'Поради']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, DORMITORY, back_button=True)


async def masters(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, VORZEL_TEXT, [], MASTERS, back_button=True, home_button=True,
                               back_home_row=True)


async def bachelors(update: Update, context: CallbackContext) -> int:
    buttons = [['На Троєщині', 'На Харківському шосе', 'На вул. Джона Маккейна']]
    return await generic_reply(update, 'Бакалаврат: Оберіть гуртожиток', buttons, BACHELORS, back_button=True,
                               home_button=True)


async def orders(update: Update, context: CallbackContext) -> int:
    buttons = [['Вартість', 'Перелік документів']]
    return await generic_reply(update, 'Поселення: Оберіть опцію', buttons, ORDERS, back_button=True, home_button=True)


async def advices(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'троя говно маккейна говно харьок топ', [], ADVICE, back_button=True,
                               home_button=True,
                               back_home_row=True)


async def troy(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, TROYA_TEXT, [], GURTO, back_button=True, home_button=True,
                               back_home_row=True)


async def kharyok(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, KHARYOK_TEXT, [], GURTO, back_button=True, home_button=True,
                               back_home_row=True)


async def makkeina(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, MAKKEINA_TEXT, [], GURTO, back_button=True, home_button=True,
                               back_home_row=True)


async def price(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'ДОРОГО', [], ORDERS_NEXT, back_button=True, home_button=True,
                               back_home_row=True)


async def document_review(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, DOCUMENTS_TEXT, [], ORDERS_NEXT, back_button=True, home_button=True,
                               back_home_row=True)


dormitory_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Гуртожитки'), dormitory)],
    states={
        DORMITORY: [
            MessageHandler(filters.Regex('Для магістрів'), masters),
            MessageHandler(filters.Regex('Для бакалаврів'), bachelors),
            MessageHandler(filters.Regex('Поселення'), orders),
            MessageHandler(filters.Regex('Поради'), advices),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        BACHELORS: [
            MessageHandler(filters.Regex('На Троєщині'), troy),
            MessageHandler(filters.Regex('На Харківському шосе'), kharyok),
            MessageHandler(filters.Regex('На вул. Джона Маккейна'), makkeina),
            MessageHandler(filters.Regex(BACK), dormitory),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        MASTERS: [
            MessageHandler(filters.Regex(BACK), dormitory),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        VORZEL: [
            MessageHandler(filters.Regex(BACK), dormitory),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        GURTO: [
            MessageHandler(filters.Regex(BACK), bachelors),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        ORDERS: [
            MessageHandler(filters.Regex('Вартість'), price),
            MessageHandler(filters.Regex('Перелік документів'), document_review),
            MessageHandler(filters.Regex(BACK), dormitory),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        ORDERS_NEXT: [
            MessageHandler(filters.Regex(BACK), orders),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        ADVICE: [
            MessageHandler(filters.Regex(BACK), dormitory),
            MessageHandler(filters.Regex(HOME), go_home),
        ]
    },
    fallbacks=[CommandHandler('start', dormitory)],
    name='dormitory-handler',
    persistent=True,
)
