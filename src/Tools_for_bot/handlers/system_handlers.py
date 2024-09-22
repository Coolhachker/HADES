from aiogram import Bot, Dispatcher
from aiogram.types import  ChatJoinRequest


def system_handlers(bot: Bot, dispatcher: Dispatcher):
    @dispatcher.chat_join_request()
    async def join_handle(request: ChatJoinRequest):
        await bot.send_message(request.chat.id, 'Бот был успешно добавлен.')