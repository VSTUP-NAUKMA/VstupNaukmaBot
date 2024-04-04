from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

from bot.utils.utils import generic_reply, go_home  # Імпорт з загального файлу

BACK = 'Назад'
HOME = 'На головну'
STUDENTLIFE, OSS, SO = range(3)

buttons = [['Органи студентського самоврядування', 'Студентські організації']]
async def student_life(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Оберіть категорію:', buttons, STUDENTLIFE, back_button=True)


async def oss(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'ск топ', [], OSS, back_button=True, home_button=True,
                               back_home_row=True)


async def so(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Сошка вступ навукма топ', [], SO, back_button=True, home_button=True,
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
    fallbacks=[],
    name='student_life-handler',
    persistent=True,
)
