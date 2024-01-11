from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

from bot.utils.utils import BACK, go_home

CONTACTS = 1


async def contacts(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Контакти', reply_markup=reply_markup)
    return CONTACTS



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
