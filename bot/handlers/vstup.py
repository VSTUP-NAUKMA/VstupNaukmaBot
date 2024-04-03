from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

from bot.utils.utils import generic_reply, go_home  # Імпорт з загального файлу

BACK = 'Назад'
HOME = 'На головну'
STUDENTLIFE, OSS, SO = range(3)


async def vstup_system(update: Update, context: CallbackContext) -> int:
    buttons = [['Опис', 'Дати вступної компанії'],
               ['Документи', 'Електронний кабінет'],
               ['Сайт приймальної комісії']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, STUDENTLIFE, back_button=True)


async def oss(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'ск топ', [], OSS, back_button=True, home_button=True,
                               back_home_row=True)


async def so(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Сошка вступ навукма топ', [], SO, back_button=True, home_button=True,
                               back_home_row=True)


vstup_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Система вступу'), vstup_system)],
    states={
        STUDENTLIFE: [
            MessageHandler(filters.Regex('Органи студентського самоврядування'), oss),
            MessageHandler(filters.Regex('Студентські організації'), so),
            MessageHandler(filters.Regex(BACK), go_home),
        ],

    },
    fallbacks=[],
    name='vstup_system',
    persistent=True,
)
