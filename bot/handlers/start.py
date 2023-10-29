from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

from bot.handlers.operator_chat import send_to_operator, IN_CONVERSATION, connect_with_operator, forward_reply_to_user

CHOOSING = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(update.message.chat_id)
    reply_keyboard = [['Бакалавр', 'Магістр'], ['Про могилянку', "Зв'язатись з оператором"]]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Hi!", reply_markup=keyboard_markup)
    return CHOOSING


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CHOOSING: [MessageHandler(filters.Regex("Зв'язатись з оператором"), connect_with_operator)],
        IN_CONVERSATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_to_operator)]
    },
    fallbacks=[CommandHandler('end', start)])
