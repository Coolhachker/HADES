from aiogram import Bot, Dispatcher
from src.Tools_for_bot.handlers import (
    text_handlers, system_handlers, callback_handlers
)
from src.Tools_for_bot.middlewares.middleware_on_new_messages import MiddlewareOnMessages
from src.Tools_for_rabbitmq.ping_pong_system import ping_the_parser
import asyncio
from dotenv import dotenv_values
bot_key = dotenv_values('src/Tools_for_bot/credentials.env').get('BOT_KEY')


class AntiSpamBot:
    def __init__(self, token):
        self.bot = Bot(token)
        self.dispatcher = Dispatcher()
        self.run_sync_functions()

    def run_sync_functions(self):
        system_handlers.system_handlers(self.bot, self.dispatcher)
        text_handlers.text_handlers(self.bot, self.dispatcher)
        callback_handlers.callbacks(self.dispatcher, self.bot)

    async def run_bot(self):
        asyncio.create_task(ping_the_parser(self.bot))
        self.dispatcher.message.middleware(MiddlewareOnMessages(self.bot))
        await self.dispatcher.start_polling(self.bot)


if __name__ == '__main__':
    bot = AntiSpamBot(bot_key)
    asyncio.run(bot.run_bot())