from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

reply_keyboard = [['Спеціальності академії', 'Система вступу'],
                  ['Студентське життя', 'Навчальний процес'],
                  ['Контакти', 'Гуртожитки'],
                  ['Чат-підтримка', 'Хочу приколюху 😜']]
keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username or str(user.id)
    first_name = user.first_name or ''
    last_name = user.last_name or ''
    phone_number = user.phone_number if hasattr(user, 'phone_number') else 'Not provided'
    user_info = f"{username}, {first_name} {last_name}, {phone_number}"

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

    if username == 'malashokk':
        await update.message.reply_text("Прівєєєт Наталка🐸", reply_markup=keyboard_markup)
    elif username == 'holychrome':
        await update.message.reply_text("Богданчик мій краш", reply_markup=keyboard_markup)
    else:
        await update.message.reply_text("Текст старт", reply_markup=keyboard_markup)


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
