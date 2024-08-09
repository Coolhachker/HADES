from src.Tools_to_save_spam_messages.save_spam_message import SaverMessages
import asyncio
import logging
from src.set_logger import ColoredFormat
from src.Tools_to_save_spam_messages.convert_to_csv import CSVConverterFromTxt
file_handler = logging.FileHandler('../../logs/spam_messages_logs.log', mode='w')
file_handler.setFormatter(ColoredFormat())

logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.DEBUG)


def handler_spam_messages(func):
    async def handler_spam(self):
        while True:
            last_message = await self.saver_messages.client.get_messages(self.saver_messages.chat, limit=1)
            if last_message[0].message == 'flag TRUE':
                logging.debug('Ожидаю новых сообщений')
                await asyncio.sleep(60)
                continue
            else:
                await func(self)
    return handler_spam


class HandlerMessages:
    def __init__(self, data_of_tg, file, file_csv):
        self.saver_messages = SaverMessages(file, **data_of_tg)
        self.path_to_file = file
        self.file_csv = file_csv
        logging.info('Постановка хендлера')

    @handler_spam_messages
    async def handle(self):
        logging.debug('Поймал новые сообщения')
        await self.saver_messages.run_case()
        converter = CSVConverterFromTxt(f'../../data/{self.path_to_file}', self.file_csv)
        converter.convert_to_csv()

    async def get_ham_messages(self):
        await self.saver_messages.get_messages_from_another_chats('configs.json')
        converter = CSVConverterFromTxt(f'../../data/{self.path_to_file}', self.file_csv)
        converter.convert_to_csv()

