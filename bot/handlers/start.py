from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

from bot.handlers.operator_chat import send_to_operator, IN_CONVERSATION, connect_with_operator

CHOOSING = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['Бакалавр', 'Магістр'], ['Про могилянку', "Чат-підтримка"]]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_text("Hi!", reply_markup=keyboard_markup)
    return CHOOSING


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CHOOSING: [MessageHandler(filters.Regex("Чат-підтримка"), connect_with_operator)],
        IN_CONVERSATION: [MessageHandler(~filters.Regex("Завершити діалог") & (
                filters.TEXT | filters.PHOTO | filters.VOICE | filters.Document.ALL | filters.ANIMATION | filters.Sticker.ALL | filters.VIDEO | filters.FORWARDED),
                                         send_to_operator)]
    },
    fallbacks=[MessageHandler(filters.Regex("Завершити діалог"), start)])
