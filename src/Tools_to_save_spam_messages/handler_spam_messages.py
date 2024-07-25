from src.Tools_to_save_spam_messages.save_spam_message import SaverMessages
import asyncio
import logging
from src.set_logger import ColoredFormat
file_handler = logging.FileHandler('../../logs/spam_messages_logs.log', mode='w')
file_handler.setFormatter(ColoredFormat())

logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.DEBUG)


def handler_spam_messages(func):
    async def handler_spam(self):
        while True:
            last_message = await self.saver_spam_messages.client.get_messages(self.saver_spam_messages.chat, limit=1)
            if last_message[0].message == 'flag TRUE':
                logging.debug('Ожидаю новых сообщений')
                await asyncio.sleep(60)
                continue
            else:
                await func(self)
    return handler_spam


class HandlerMessages:
    def __init__(self, data_of_tg, file):
        self.saver_messages = SaverMessages(file, **data_of_tg)
        self.path_to_file = file
        logging.info('Постановка хендлера')

    @handler_spam_messages
    async def handle(self):
        logging.debug('Поймал новые сообщения')
        await self.saver_messages.run_case()