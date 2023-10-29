import os

from telegram import Update, Message
from telegram.ext import CallbackContext, MessageHandler, filters

CHAT_WITH_OPERATOR = 1
IN_CONVERSATION = 2


async def connect_with_operator(update: Update, _: CallbackContext) -> int:
    await update.message.reply_text(
        "Для початку діалогу з оператором, відправ повідмолення та очікуй відповіді. Для завершення чату натисни /end")
    return IN_CONVERSATION


async def send_to_operator(update: Update, _: CallbackContext) -> int:
    support_chat_id = os.getenv('TELEGRAM_SUPPORT_CHAT_ID')
    await update.message.forward(
        chat_id=support_chat_id,
    )
    return IN_CONVERSATION


async def forward_reply_to_user(update: Update, _: CallbackContext) -> None:
    print("forward_reply_to_user function has been called")

    message: Message = update.message
    if message.reply_to_message is not None:
        to_chat_id = message.reply_to_message.forward_from.id
        if message.text is not None:
            await _.bot.send_message(chat_id=to_chat_id, text=message.text)
        elif message.photo is not None and len(message.photo) > 0:
            photo_file_id = message.photo[-1].file_id
            caption = message.caption
            await _.bot.send_photo(chat_id=to_chat_id, photo=photo_file_id, caption=caption)
        elif message.animation is not None:
            animation_file_id = message.animation.file_id
            caption = message.caption
            await _.bot.send_animation(chat_id=to_chat_id, animation=animation_file_id, caption=caption)
        # Add other content types like stickers, video, etc...
        else:
            print(f"Unsupported message type: {message}")


reply_handler = MessageHandler(filters.REPLY, forward_reply_to_user)
