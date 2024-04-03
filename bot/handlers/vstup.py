from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

from bot.utils.utils import generic_reply, go_home  # Імпорт з загального файлу

BACK = 'Назад'
HOME = 'На головну'
VSTUP, VSTUP_END = range(2)


async def vstup_system(update: Update, context: CallbackContext) -> int:
    print("asd123")
    buttons = [['Опис', 'Дати вступної кампанії'],
               ['Документи', 'Електронний кабінет'],
               ['Сайт приймальної комісії']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, VSTUP, back_button=True)


async def descr(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'ск топ', [], VSTUP_END, back_button=True, home_button=True,
                               back_home_row=True)


async def dates(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Сошка вступ навукма топ', [], VSTUP_END, back_button=True, home_button=True,
                               back_home_row=True)


async def cabinet(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Сошка вступ навукма топ', [], VSTUP_END, back_button=True, home_button=True,
                               back_home_row=True)


async def documents(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Сошка вступ навукма топ', [], VSTUP_END, back_button=True, home_button=True,
                               back_home_row=True)


async def site(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Сошка вступ навукма топ', [], VSTUP_END, back_button=True, home_button=True,
                               back_home_row=True)


vstup_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Система вступу'), vstup_system)],
    states={
        VSTUP: [
            MessageHandler(filters.Regex('Опис'), descr),
            MessageHandler(filters.Regex('Дати вступної кампанії'), dates),
            MessageHandler(filters.Regex('Електронний кабінет'), cabinet),
            MessageHandler(filters.Regex('Документи'), documents),
            MessageHandler(filters.Regex('Сайт приймальної комісії'), site),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        VSTUP_END: [
            MessageHandler(filters.Regex(BACK), vstup_system),
            MessageHandler(filters.Regex(HOME), go_home),
        ]

    },
    fallbacks=[],
    name='vstup_handler',
    persistent=True,
)
