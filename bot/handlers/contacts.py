from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters, CommandHandler

from bot.handlers.operator_chat import go_home
from bot.handlers.start import fresh_start
from bot.utils.fields import CONTACTS_TEXT
from bot.utils.utils import generic_reply, unlucky

BACK = 'Назад'
HOME = 'На головну'
CONTACTS = 1


async def contacts(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, CONTACTS_TEXT, [], CONTACTS, back_button=True,
                               back_home_row=True)


contacts_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Контакти'), contacts)],
    states={
        CONTACTS: [
            MessageHandler(filters.Regex(BACK), go_home),
        ],

    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start),
               MessageHandler(filters.TEXT, unlucky)],
    name='contacts-handler',
    persistent=True,
)
