import re
from aiogram import Dispatcher, Bot
from aiogram.types import CallbackQuery


def callbacks(dispatcher: Dispatcher, bot: Bot):
    @dispatcher.callback_query(lambda cq: re.search('&', cq.data))
    async def callback_on_ban_spam_message(cq: CallbackQuery):
        chat_id = cq.data.split('&')[0]
        message_id = int(cq.data.split('&')[1])
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(cq.message.chat.id, 'Сообщение было удалено.')
        await bot.delete_message(cq.message.chat.id, cq.message.message_id)

    @dispatcher.callback_query(lambda cq: cq.data == 'pass')
    async def callback_on_pass(cq: CallbackQuery):
        await bot.delete_message(cq.message.chat.id, cq.message.message_id)
