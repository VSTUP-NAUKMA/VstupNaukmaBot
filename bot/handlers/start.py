from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from bot.utils.fields import START_TEXT

reply_keyboard = [['Спеціальності академії', 'Навчальний процес'],
                  ['Студентське життя', 'Гуртожитки' ],
                  ['Контакти', 'Чат-підтримка'],
                  ['Хочу приколюху 😜']]
keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username or str(user.id)
    first_name = user.first_name or ''
    last_name = user.last_name or ''
    user_info = f"{username}, {first_name} {last_name}"

    file_path = "./usernames.txt"
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            existing_users = set(file.read().splitlines())
    except FileNotFoundError:
        existing_users = set()

    if user_info not in existing_users:
        with open(file_path, "a", encoding='utf-8') as file:
            file.write(user_info + "\n")
            existing_users.add(user_info)

    await update.message.reply_text(START_TEXT, reply_markup=keyboard_markup)


async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
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
