from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


def set_soam_markup(message_id: int, chat_id: int, url: str):
    builder = InlineKeyboardBuilder()

    button_check_message = InlineKeyboardButton(text='🔎 Посмотреть сообщение', url=url)
    button_ban_message = InlineKeyboardButton(text='✅️ БАН', callback_data=f'{chat_id}&{message_id}')
    button_pass = InlineKeyboardButton(text='❗ Пропустить', callback_data='pass')

    builder.row(button_check_message)
    builder.row(button_ban_message)
    builder.row(button_pass)

    return builder.as_markup()