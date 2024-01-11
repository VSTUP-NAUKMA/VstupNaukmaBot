from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from bot.handlers.dormitory import dormitory, BACK, go_home
from bot.handlers.operator_chat import connect_with_operator
from bot.handlers.admission import admission

CHOOSING, DORMITORY, IN_CONVERSATION = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Вступ на навчання', 'Навчальний процес', 'Гуртожитки'],
                      ['Студентське життя', 'Контакти', 'Чат-підтримка']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_text("Hi!", reply_markup=keyboard_markup)


start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CHOOSING: [],
    },
    fallbacks=[MessageHandler(filters.Regex(BACK), go_home)],
    map_to_parent={
        CHOOSING: CHOOSING,
        ConversationHandler.END: ConversationHandler.END
    },
    name="main-handler",
    persistent=True,
)
