from aiogram import Bot, Dispatcher
from aiogram.types import Message, ChatJoinRequest


def text_handlers(bot: Bot, dispatcher: Dispatcher):
    @dispatcher.message()
    async def new_text_message(message: Message):
        await bot.send_message(message.chat.id, 'Здарова.')
