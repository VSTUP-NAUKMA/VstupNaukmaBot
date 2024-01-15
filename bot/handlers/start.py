from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

CHOOSING = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Вступ на навчання', 'Навчальний процес', 'Гуртожитки'],
                      ['Студентське життя', 'Контакти', 'Чат-підтримка']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Обери потрібний розділ", reply_markup=keyboard_markup)


start_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('start'), start)],
    states={
    },
    fallbacks=[],
    name="main-handler",
    persistent=True,
)
