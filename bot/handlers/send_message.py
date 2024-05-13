from telegram import Update, ForceReply
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

GET_MESSAGE, CONFIRMATION = range(2)


async def start_broadcast(update: Update, context: CallbackContext) -> int:
    if update.effective_user.username == 'zhenyettta':
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
        for chat_id in chat_ids:
            print(chat_id)
            await context.bot.send_message(chat_id=chat_id, text=message)
        await update.message.reply_text('Повідомлення відправлено всім користувачам.')
    else:
        await update.message.reply_text('Розсилка скасована.')
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
