from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


def set_soam_markup(message_id: int, chat_id: int):
    builder = InlineKeyboardBuilder()

    button_check_message = InlineKeyboardButton(text='🔎 Посмотреть сообщение', url=f'https://t.me/c/{chat_id}/{message_id}')
    button_ban_message = InlineKeyboardButton(text='✅️ БФН', callback_data=f'{message_id}-{message_id}')
    button_pass = InlineKeyboardButton(text='❗ Пропустить')

    builder.row(button_check_message)
    builder.row(button_ban_message)
    builder.row(button_pass)

    return builder.as_markup()