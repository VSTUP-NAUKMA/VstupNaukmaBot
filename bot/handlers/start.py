from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackContext


reply_keyboard = [['Вступ на навчання', 'Система вступу'],
                  ['Студентське життя', 'Навчальний процес'],
                  ['Контакти', 'Гуртожитки'],
                  ['Чат-підтримка', 'Хочу приколюху 😜']]
keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username
    if username:
        with open("./usernames.txt", "a") as file:
            file.write(username + "\n")
    else:
        with open("./usernames.txt", "a") as file:
            file.write(str(user.id) + "\n")
    await update.message.reply_text("Текст старт", reply_markup=keyboard_markup)


async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Обери потрібний розділ", reply_markup=keyboard_markup)


async def fresh_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Ваші дані та стан були успішно скинуті. Почнемо знову!")
    await start(update, context)
    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('start'), start)],
    states={
    },
    fallbacks=[],
    name="main-handler",
    persistent=True,
)
