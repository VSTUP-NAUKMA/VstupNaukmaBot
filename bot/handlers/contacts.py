from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

from bot.handlers.operator_chat import go_home
from bot.utils.fields import CONTACTS_TEXT
from bot.utils.utils import generic_reply

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
    fallbacks=[],
    name='contacts-handler',
    persistent=True,
)
