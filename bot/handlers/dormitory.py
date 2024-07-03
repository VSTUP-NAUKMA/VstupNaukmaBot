import os

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, filters

from bot.handlers.start import fresh_start
from bot.utils.fields import *
from bot.utils.utils import generic_reply, go_home, unlucky

BACK = 'Назад'
HOME = 'На головну'
DORMITORY, MASTERS, BACHELORS, ORDERS, PRICE, GURTO, DOCUMENT_REVIEW, VORZEL, ADVICE, ORDERS_NEXT = range(10)


async def dormitory(update: Update, context: CallbackContext) -> int:
    TELEGRAM_SUPPORT_CHAT_ID = os.getenv('TELEGRAM_SUPPORT_CHAT_ID')
    chat_id = update.message.chat_id
    if int(chat_id) == int(TELEGRAM_SUPPORT_CHAT_ID):
        return
    buttons = [['Для бакалаврів', 'Для магістрів'], ['Поселення', 'Поради']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, DORMITORY, back_button=True)


async def masters(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, VORZEL_TEXT, [], MASTERS, back_button=True, home_button=True,
                               back_home_row=True)


async def bachelors(update: Update, context: CallbackContext) -> int:
    buttons = [['Троєщина', 'Харківське шосе', 'Джона Маккейна']]
    return await generic_reply(update, 'Оберіть гуртожиток:', buttons, BACHELORS, back_button=True,
                               home_button=True)


async def orders(update: Update, context: CallbackContext) -> int:
    buttons = [['Поселення, вартість та оплата', 'Перелік документів']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, ORDERS, back_button=True, home_button=True)


async def advices(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, ADVICES_TEXT, [], ADVICE, back_button=True,
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
    return await generic_reply(update, PRICE_TEXT, [], ORDERS_NEXT, back_button=True, home_button=True,
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
            MessageHandler(filters.Regex('Троєщина'), troy),
            MessageHandler(filters.Regex('Харківське шосе'), kharyok),
            MessageHandler(filters.Regex('Джона Маккейна'), makkeina),
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
            MessageHandler(filters.Regex('Поселення, вартість та оплата'), price),
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
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start), MessageHandler(filters.TEXT, unlucky)],
    name='dormitory-handler',
    persistent=True,
)
