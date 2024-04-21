from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters, CommandHandler

from bot.handlers.start import fresh_start
from bot.utils.fields import STUDENTSORG_TEXT, STUDENTSOSS_TEXT
from bot.utils.utils import generic_reply, go_home, unlucky  # Імпорт з загального файлу

BACK = 'Назад'
HOME = 'На головну'
STUDENTLIFE, OSS, SO = range(3)

buttons = [['Органи студентського самоврядування', 'Студентські організації']]


async def student_life(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Оберіть категорію:', buttons, STUDENTLIFE, back_button=True)


async def oss(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, STUDENTSOSS_TEXT, [], OSS, back_button=True, home_button=True,
                               back_home_row=True)


async def so(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, STUDENTSORG_TEXT, [], SO, back_button=True, home_button=True,
                               back_home_row=True)


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
        SO: [
            MessageHandler(filters.Regex(BACK), student_life),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
    },
    fallbacks=[CommandHandler('reset', fresh_start), MessageHandler(filters.TEXT, unlucky)],
    name='student_life-handler',
    persistent=True,
)
