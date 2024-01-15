from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

from bot.utils.repository import generic_reply, go_home

BACK = 'Назад'
HOME = 'На головну'
CONTACTS = 1


async def contacts(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Контакти текст', [], CONTACTS, back_button=True,
                               back_home_row=True)


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
