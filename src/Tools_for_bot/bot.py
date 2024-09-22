from aiogram import Bot, Dispatcher
from src.Tools_for_bot.handlers import (
    text_handlers, system_handlers
)
from src.Tools_for_bot.middlewares.middleware_on_new_messages import MiddlewareOnMessages
import asyncio


class AntiSpamBot:
    def __init__(self, token):
        self.bot = Bot(token)
        self.dispatcher = Dispatcher()
        self.run_sync_functions()

    def run_sync_functions(self):
        text_handlers.text_handlers(self.bot, self.dispatcher)
        system_handlers.system_handlers(self.bot, self.dispatcher)

    async def run_bot(self):
        self.dispatcher.message.middleware(MiddlewareOnMessages(self.bot))
        await self.dispatcher.start_polling(self.bot)


if __name__ == '__main__':
    bot = AntiSpamBot('7053562789:AAEF1X5gMgTgfyTTdcvKziHp7hxkDbEgK6U')
    asyncio.run(bot.run_bot())