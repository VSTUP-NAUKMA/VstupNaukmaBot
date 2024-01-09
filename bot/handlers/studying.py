from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

BACK = 'Назад'
HOME = 'На головну'
BACHELOR, FACULTY = range(2)


async def contacts(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Бакалаврат')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Вступ на навчання: оберіть опцію', reply_markup=reply_markup)
    return BACHELOR


async def faculties(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Факультети і спеціальності')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Оберіть факультет', reply_markup=reply_markup)
    return FACULTY

async def faculties(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='ФІ')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Оберіть факультет', reply_markup=reply_markup)
    return FACULTY


async def go_home(update: Update, context: CallbackContext) -> int:
    from bot.handlers.start import start
    await start(update, context)
    return ConversationHandler.END


# Структура ConversationHandler
studying = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Контакти'), contacts)],
    states={
        BACHELOR: [
            MessageHandler(filters.Regex(BACK), go_home),
            MessageHandler(filters.Regex('Бакалаврат'), faculties),
        ],
        FACULTY: [
            MessageHandler(filters.Regex(BACK), faculties),
            MessageHandler(filters.Regex('Факультети і спеціальності'), faculties),
        ]

    },
    fallbacks=[],
    name='contacts-handler',
    persistent=True,
)
