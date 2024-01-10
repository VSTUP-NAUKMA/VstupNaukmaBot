import asyncio
import os

from telegram import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, MessageHandler, filters, ConversationHandler

from bot.utils.config import logger

IN_CONVERSATION = 1
pending_replies = {}


async def clear_pending_replies(interval: int):
    while True:
        await asyncio.sleep(interval)
        pending_replies.clear()
        logger.info('Cleared pending_replies')


async def go_home(update: Update, context: CallbackContext) -> int:
    from bot.handlers.start import start
    await start(update, context)
    return ConversationHandler.END


async def connect_with_operator(update: Update, _: CallbackContext) -> int:
    keyboard = [
        [
            KeyboardButton('Завершити діалог'),
        ]
    ]
    keyboard_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        'Для початку діалогу з оператором, відправ повідомлення та очікуй відповіді. Для завершення діалогу натисни '
        '"Завершити діалог".',
        reply_markup=keyboard_markup)
    return IN_CONVERSATION


async def unsuported_type(update: Update, _: CallbackContext) -> int:
    support_chat_id = os.getenv('TELEGRAM_SUPPORT_CHAT_ID')
    message: Message = update.message
    message_type = str(type(message))
    await _.bot.send_message(chat_id=support_chat_id, text='Я ' + message_type + ' не підтримую)')
    return IN_CONVERSATION


async def send_to_operator(update: Update, _: CallbackContext) -> int:
    # TELEGRAM_SUPPORT_CHAT_ID=-1002086897896
    support_chat_id = os.getenv('TELEGRAM_SUPPORT_CHAT_ID')
    user = update.message.from_user
    username = f'@{user.username}' if user.username else 'Без ніку 😭'
    message: Message = update.message
    message_caption = message.caption if message.caption is not None else ""
    caption = f'{username}'

    button = InlineKeyboardButton(text='Не вибрано', callback_data='not_pressed')
    reply_markup = InlineKeyboardMarkup([[button]])

    if message.text is not None:
        sent_message = await _.bot.send_message(chat_id=support_chat_id, text=f'{caption}\n{message.text}',
                                                reply_markup=reply_markup)
    elif message.photo is not None and len(message.photo) > 0:
        sent_message = await _.bot.send_photo(chat_id=support_chat_id, photo=message.photo[-1].file_id,
                                              caption=f'{caption}\n{message_caption}', reply_markup=reply_markup)
    elif message.animation:
        sent_message = await _.bot.send_animation(chat_id=support_chat_id, animation=message.animation.file_id,
                                                  caption=f'{caption}\n', reply_markup=reply_markup)
    elif message.sticker:
        sent_message = await _.bot.send_sticker(chat_id=support_chat_id, sticker=message.sticker.file_id,
                                                reply_markup=reply_markup)
    elif message.voice:
        sent_message = await _.bot.send_voice(chat_id=support_chat_id, voice=message.voice.file_id, caption=caption,
                                              reply_markup=reply_markup)
    elif message.video:
        sent_message = await _.bot.send_video(chat_id=support_chat_id, video=message.video.file_id, caption=caption,
                                              reply_markup=reply_markup)
    elif message.location:
        sent_message = await _.bot.send_location(chat_id=support_chat_id, latitude=message.location.latitude,
                                                 longitude=message.location.longitude,
                                                 reply_markup=reply_markup)
    elif message.video_note:
        await _.bot.send_message(chat_id=support_chat_id, text=caption)
        sent_message = await _.bot.send_video_note(chat_id=support_chat_id, video_note=message.video_note,
                                                   reply_markup=reply_markup)

    elif message.document:
        sent_message = await _.bot.send_document(chat_id=support_chat_id, document=message.document.file_id,
                                                 caption=f'{caption}\n{message_caption}', reply_markup=reply_markup)

    pending_replies[sent_message.message_id] = update.effective_chat.id

    return IN_CONVERSATION


async def button_callback(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'already_pressed':
        await query.answer('А всьо не можна більше :(')
        return
    if query.data == 'not_pressed':
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=query.from_user.username, callback_data='already_pressed')]]))


async def forward_reply_to_user(update: Update, _: CallbackContext) -> None:
    message: Message = update.message
    reply_to_id = extract_reply_id(message)

    if reply_to_id:
        to_chat_id = pending_replies.get(reply_to_id)
        if message.text:
            await send_message(_, to_chat_id, text=message.text)
        elif message.photo:
            await send_photo(_, to_chat_id, message)
        elif message.animation:
            await send_animation(_, to_chat_id, message)
        elif message.sticker:
            await send_sticker(_, to_chat_id, message)
        elif message.document:
            await send_document(_, to_chat_id, message)
        elif message.video:
            await send_video(_, to_chat_id, message)
        elif message.location:
            await send_location(_, to_chat_id, message)
        elif message.voice:
            await send_voice(_, to_chat_id, message)
        else:
            print(f'Unsupported message type: {message}')


def extract_reply_id(message):
    return message.reply_to_message.message_id if message.reply_to_message else None


async def send_message(_, chat_id, text=None):
    if text:
        await _.bot.send_message(chat_id=chat_id, text=text)


async def send_photo(_, chat_id, message):
    if len(message.photo) > 0:
        photo_file_id = message.photo[-1].file_id
        await _.bot.send_photo(chat_id=chat_id, photo=photo_file_id, caption=message.caption)


async def send_animation(_, chat_id, message):
    animation_file_id = message.animation.file_id
    await _.bot.send_animation(chat_id=chat_id, animation=animation_file_id, caption=message.caption)


async def send_sticker(_, chat_id, message):
    sticker_file_id = message.sticker.file_id
    await _.bot.send_sticker(chat_id=chat_id, sticker=sticker_file_id)


async def send_document(_, chat_id, message):
    await _.bot.send_document(chat_id=chat_id, document=message.document.file_id, caption=message.caption)


async def send_video(_, chat_id, message):
    await _.bot.send_video(chat_id=chat_id, video=message.document.file_id, caption=message.caption)


async def send_location(_, chat_id, message):
    await _.bot.send_location(chat_id=chat_id, latitude=message.location.latitude, longitude=message.location.longitude,
                              caption=message.caption)


async def send_voice(_, chat_id, message):
    await _.bot.send_voice(chat_id=chat_id, voice=message.voice.file_id)


operator_chat_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Чат-підтримка'), connect_with_operator)],
    states={
        IN_CONVERSATION: [
            MessageHandler(~filters.Regex('Завершити діалог') & (
                    filters.TEXT | filters.PHOTO | filters.VOICE | filters.Document.ALL |
                    filters.ANIMATION | filters.Sticker.ALL | filters.VIDEO | filters.FORWARDED | filters.VIDEO | filters.LOCATION | filters.VIDEO_NOTE),
                           send_to_operator),
            MessageHandler(filters.Regex('Завершити діалог'), go_home),
        ],
    },
    fallbacks=[MessageHandler(filters.ALL, unsuported_type)],
    name='operator_chat-handler',
    persistent=True,
)
reply_handler = MessageHandler(filters.REPLY, forward_reply_to_user)
