import telegram
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

GET_MESSAGE, CONFIRMATION = range(2)
reply_keyboard = [['Спеціальності Академії', 'Система вступу'],
                  ['Студентське життя', 'Навчальний процес'],
                  ['Контакти', 'Гуртожитки'],
                  ['Чат-підтримка', 'Хочу приколюху 😜']]
keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


async def start_broadcast(update: Update, context: CallbackContext) -> int:
    if update.effective_user.username in ['zhenyettta', 'malashokk']:
        await update.message.reply_text('Введіть повідомлення для розсилки:', reply_markup=ForceReply(selective=True))
        return GET_MESSAGE
    else:
        await update.message.reply_text('Ви не маєте прав на виконання цієї команди.')
        return ConversationHandler.END


async def get_message(update: Update, context: CallbackContext) -> int:
    context.user_data['message'] = update.message.text
    await update.message.reply_text('Ви впевнені, що хочете відправити це повідомлення всім користувачам? (так/ні)')
    return CONFIRMATION


async def send_broadcast(update: Update, context: CallbackContext) -> int:
    answer = update.message.text.lower()
    if answer == 'так':
        message = context.user_data['message']
        chat_ids = read_chat_ids('usernames.txt')
        success_count = 0
        fail_count = 0
        for chat_id in chat_ids:
            try:
                await context.bot.send_message(chat_id=chat_id, text=message)
                success_count += 1
            except telegram.error.Forbidden:
                fail_count += 1
                print(f"Failed to send message to {chat_id}: bot was blocked by the user")
            except Exception as e:
                fail_count += 1
                print(f"Failed to send message to {chat_id}: {e}")

        await update.message.reply_text(f'Повідомлення відправлено {success_count} користувачам. '
                                        f'Не вдалося відправити {fail_count} користувачам.', reply_markup=keyboard_markup)
    else:
        await update.message.reply_text('Розсилка скасована.', reply_markup=keyboard_markup)
    return ConversationHandler.END


def read_chat_ids(filename):
    chat_ids = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            chat_id = line.split(',')[0].strip()
            if chat_id.isdigit():
                chat_ids.append(chat_id)
            else:
                print(f"Попередження: Невірний chat_id виявлено ({chat_id}), який був пропущений.")
    return chat_ids


broadcast_handler = ConversationHandler(
    entry_points=[CommandHandler('broadcast', start_broadcast)],
    states={
        GET_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
        CONFIRMATION: [MessageHandler(filters.Regex('^(так|ні)$'), send_broadcast)]
    },
    fallbacks=[CommandHandler('cancel', lambda update, context: update.message.reply_text(
        'Розсилка скасована.') & ConversationHandler.END)]
)
