from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

BACK = 'Назад'
HOME = 'На головну'
STUDENTLIFE, OSS, SO = range(3)


async def student_life(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton(text='Органи студентського самоврядування'),
         KeyboardButton(text='Студентські організації')],
        [KeyboardButton(text='Назад')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Оберіть категорію:', reply_markup=reply_markup)
    return STUDENTLIFE


def get_keyboard(*row_buttons, back_button=False):
    keyboard = [list(map(KeyboardButton, row)) for row in row_buttons]
    if back_button:
        keyboard.append([KeyboardButton(BACK)])
        keyboard.append([KeyboardButton(HOME)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def go_home(update: Update, context: CallbackContext) -> int:
    from bot.handlers.start import start
    await start(update, context)
    return ConversationHandler.END


async def oss(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text('ск топ', reply_markup=reply_markup)
    return OSS


async def so(update: Update, context: CallbackContext) -> int:
    reply_markup = get_keyboard([], back_button=True)
    await update.message.reply_text('Сошка вступ навукма топ', reply_markup=reply_markup)
    return SO


# Структура ConversationHandler
student_life_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Студентське життя'), student_life)],
    states={
        STUDENTLIFE: [
            MessageHandler(filters.Regex('Органи студентського самоврядування'), oss),
            MessageHandler(filters.Regex('Студентські організації'), so),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        OSS: [
            MessageHandler(filters.Regex(BACK), student_life),
            MessageHandler(filters.Regex(HOME), go_home),
        ],

        SO: [MessageHandler(filters.Regex(BACK), student_life),
             MessageHandler(filters.Regex(HOME), go_home),
             ],

    },
    fallbacks=[],
    name='student_life-handler',
    persistent=True,
)
