from aiogram import Bot, Dispatcher
from aiogram.types import Message
import re


def text_handlers(bot: Bot, dispatcher: Dispatcher):
    @dispatcher.message(lambda message: message.text and re.search('/hades', message.text) is None)
    async def new_text_message(message: Message):
        await bot.send_message(message.chat.id, 'Здарова.')
