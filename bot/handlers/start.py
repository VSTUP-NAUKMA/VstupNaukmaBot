from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

from bot.handlers.dormitory import dormitory, dormitory_handler, BACK, go_back
from bot.handlers.operator_chat import conv_handler, connect_with_operator

CHOOSING, DORMITORY, IN_CONVERSATION = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Вступ на навчання', 'Навчальний процес', 'Гуртожитки'],
                      ['Студентське життя', 'Контакти', 'Чат-підтримка']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_text("Hi!", reply_markup=keyboard_markup)


start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CHOOSING: [
            MessageHandler(filters.Regex('Гуртожитки'), dormitory),
            MessageHandler(filters.Regex('Чат-підтримка'), connect_with_operator),
            # ...
        ],
    },
    fallbacks=[MessageHandler(filters.Regex(BACK), go_back)],
    map_to_parent={
        CHOOSING: CHOOSING,
        ConversationHandler.END: ConversationHandler.END
    }
)
