from aiogram import Bot, Dispatcher
from aiogram.types import Message
import re
from src.Tools_for_rabbitmq.producer import producer
from src.databases.mysqldb import client_mysqldb
from src.Tools_for_bot.buttons.spam_message_markup import set_soam_markup


def text_handlers(bot: Bot, dispatcher: Dispatcher):
    @dispatcher.message(lambda message: message.text and re.search('/hades', message.text) is None)
    async def new_text_message(message: Message):
        result = producer.publish(message=message.text)
        if bool(result) is True:
            admin = client_mysqldb.get_chat_id_of_admin(message.chat.id)
            await bot.send_message(admin, '⚠️ Бот распознал следующее сообщение, как спам:\n\n'+message.text, reply_markup=set_soam_markup(message.message_id, message.chat.id))
        else:
            pass
