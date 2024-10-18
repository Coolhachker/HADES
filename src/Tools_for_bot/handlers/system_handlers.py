from aiogram import Bot, Dispatcher
from aiogram.types import Message
from src.Tools_for_bot.templates import first_message
from src.databases.mysqldb import client_mysqldb


def system_handlers(bot: Bot, dispatcher: Dispatcher):
    @dispatcher.message(lambda message: message.new_chat_members is not None and message.new_chat_members[0].username == 'Hades_for_chats_bot')
    async def join_handle(message: Message):
        admin_who_added_the_bot = message.from_user.id
        client_mysqldb.add_entry_in_admins(admin_who_added_the_bot, message.chat.id, message.from_user.username)
        await bot.send_message(message.chat.id, first_message % message.chat.title)