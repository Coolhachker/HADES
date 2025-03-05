from aiogram import BaseMiddleware, Bot


class MiddlewareOnMessages(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(self, handler, event, data):
        if str(event.chat.id).startswith('-'):
            await handler(event, data)
        else:
            await self.bot.send_message(event.chat.id, 'Бот работает только в группах.')
