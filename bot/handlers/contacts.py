from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

BACK = 'Назад'
HOME = 'На головну'
CONTACTS = 1


async def contacts(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Контакти', reply_markup=reply_markup)
    return CONTACTS


async def go_home(update: Update, context: CallbackContext) -> int:
    from bot.handlers.start import start
    await start(update, context)
    return ConversationHandler.END


# Структура ConversationHandler
contacts_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Контакти'), contacts)],
    states={
        CONTACTS: [
            MessageHandler(filters.Regex(BACK), go_home),
        ],

    },
    fallbacks=[],
    name='contacts-handler',
    persistent=True,
)
