from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

CHOOSING = 1
GET_USER_INPUT = 2


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['Бакалавр', 'Магістр'], ['Про могилянку', "Зв'язатись з оператором"]]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Hi!", reply_markup=keyboard_markup)
    return GET_USER_INPUT




async def get_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    # Now you can process user_input
    await update.message.reply_text(f"You said: {user_input}")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GET_USER_INPUT: [
            MessageHandler(filters.TEXT, get_user_input)]
    },
    fallbacks=[]
)
