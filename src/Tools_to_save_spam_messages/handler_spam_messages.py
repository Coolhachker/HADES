from src.Tools_to_save_spam_messages.save_spam_message import SaverSpamMessages
import asyncio
import logging
logging.basicConfig(filename='../../logs/spam_messages_logs', filemode='w', level=logging.DEBUG, format=f'[%(asctime)s]-[%(levelname)s]-"%(message)s"')


class HandlerSpamMessages:
    def __init__(self, data_of_tg):
        self.saver_spam_messages = SaverSpamMessages(**data_of_tg)
        logging.info('Постановка хендлера')

    async def handle(self):
        while True:
            last_message = await self.saver_spam_messages.client.get_messages(self.saver_spam_messages.chat, limit=1)
            if last_message[0].message == 'flag TRUE':
                logging.debug('Ожидаю новых сообщений')
                await asyncio.sleep(60)
                continue
            else:
                logging.debug('Поймал новые сообщения')
                await self.saver_spam_messages.run_case()
                continue


if __name__ == '__main__':
    data = {'api_id': 19567654, 'api_hash': '7ec7d44a4889e041dd667dc760b323e1', 'session_name': 'session'}
    handler = HandlerSpamMessages(data)
    asyncio.get_event_loop().run_until_complete(handler.handle())