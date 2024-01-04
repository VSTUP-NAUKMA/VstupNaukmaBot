from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from bot.utils.fields import *

BACK = 'Назад'
HOME = 'На головну'
(DORMITORY, MASTERS, BACHELORS, FINALIZING, ORDERS, PRICE, GURTO, DOCUMENT_REVIEW, VORZEL, ADVICE, ORDERS_NEXT) = range(11)


async def dormitory(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Для магістрів')],
        [KeyboardButton(text='Для бакалаврів')],
        [KeyboardButton(text='Поселення')],
        [KeyboardButton(text='Поради')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Оберіть категорію:', reply_markup=reply_markup)
    return DORMITORY


def get_keyboard(*row_buttons, back_button=False):
    keyboard = [list(map(KeyboardButton, row)) for row in row_buttons]
    if back_button:
        keyboard.append([KeyboardButton(BACK)])
        keyboard.append([KeyboardButton(HOME)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def go_home(update: Update, context: CallbackContext) -> int:
    from bot.handlers.start import start
    await start(update, context)
    return ConversationHandler.END


async def masters(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard(['У смт Ворзель'], back_button=True)
    await update.message.reply_text('Магістратура: Оберіть гуртожиток', reply_markup=reply_markup)
    return MASTERS


async def bachelors(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard(['На Троєщині', 'На Харківському шосе', 'На вул. Джона Маккейна'], back_button=True)
    await update.message.reply_text('Бакалаврат: Оберіть гуртожиток', reply_markup=reply_markup)
    return BACHELORS


async def orders(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard(['Вартість', 'Перелік документів'], back_button=True)
    await update.message.reply_text('Поселення: Оберіть опцію', reply_markup=reply_markup)
    return ORDERS


async def advices(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text("троя говно маккейна говно харьок топ", reply_markup=reply_markup)
    return ADVICE


async def troy(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text(TROYA_TEXT, reply_markup=reply_markup)
    return GURTO


async def vorzel(update: Update, context: CallbackContext):
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text(VORZEL_TEXT, reply_markup=reply_markup)
    return VORZEL


async def kharyok(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text(KHARYOK_TEXT, reply_markup=reply_markup)
    return GURTO


async def makkeina(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text(MAKKEINA_TEXT, reply_markup=reply_markup)
    return GURTO


async def price(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text("ДОРОГО", reply_markup=reply_markup)
    return ORDERS_NEXT


async def document_review(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text(DOCUMENTS_TEXT, reply_markup=reply_markup)
    return ORDERS_NEXT


# Структура ConversationHandler
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
            MessageHandler(filters.Regex('У смт Ворзель'), vorzel),
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
)
