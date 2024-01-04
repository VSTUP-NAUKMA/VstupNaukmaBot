from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from bot.utils.fields import VORZEL_TEXT

BACK = 'Назад'
HOME = 'На головну'
(DORMITORY, MASTERS, BACHELORS, FINALIZING, ORDERS, PRICE, TROY, KHARYOK, MAKKEINA, DOCUMENT_REVIEW, VORZEL, ADVICE) = range(12)


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


async def go_back(update: Update, context: CallbackContext) -> int:
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
    # ...
    return BACHELORS



async def orders(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Вартість')],
        [KeyboardButton(text='Перелік документів')],
        [KeyboardButton(text='Назад')]

    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Поселення: Оберіть опцію', reply_markup=reply_markup)
    return ORDERS

async def advices(update: Update, context: CallbackContext) -> int:
    # ...
    return DORMITORY

async def troy(update: Update, context: CallbackContext) -> int:
    # ...
    await dormitory(update, context)
    return DORMITORY


async def vorzel(update: Update, context: CallbackContext):
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text(VORZEL_TEXT, reply_markup=reply_markup)



async def kharyok(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard([], back_button=True)
    return DORMITORY


async def makkeina(update: Update, context: CallbackContext) -> int:
    # ...
    await dormitory(update, context)
    return DORMITORY


async def price(update: Update, context: CallbackContext) -> int:
    # ...
    await dormitory(update, context)
    return DORMITORY


async def document_review(update: Update, context: CallbackContext) -> int:
    # ...
    await dormitory(update, context)
    return DORMITORY


# Структура ConversationHandler
dormitory_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Гуртожитки'), dormitory)],
    states={
        DORMITORY: [
            MessageHandler(filters.Regex('Для магістрів'), masters),
            MessageHandler(filters.Regex('Для бакалаврів'), bachelors),
            MessageHandler(filters.Regex('Поселення'), orders),
            MessageHandler(filters.Regex('Поради'), advices),
            MessageHandler(filters.Regex(BACK), go_back),
        ],
        BACHELORS: [
            MessageHandler(filters.Regex('На Троєщині'), troy),
            MessageHandler(filters.Regex('На Харківському шосе'), kharyok),
            MessageHandler(filters.Regex('На вул. Джона Маккейна'), makkeina),
            MessageHandler(filters.Regex(BACK), dormitory),
            MessageHandler(filters.Regex(HOME), go_back),
        ],

        MASTERS: [
            MessageHandler(filters.Regex('У смт Ворзель'), vorzel),
            MessageHandler(filters.Regex(BACK), dormitory),
            MessageHandler(filters.Regex(HOME), go_back),
        ],
    },
    fallbacks=[CommandHandler('start', dormitory)],
)
