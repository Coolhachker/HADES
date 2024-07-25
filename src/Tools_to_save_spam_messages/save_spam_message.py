from telethon import TelegramClient
import re
import logging
logger = logging.getLogger(__name__)


class SaverMessages:
    def __init__(self, file, api_id, api_hash, session_name):
        self.chat = 'https://t.me/kefvkeve'
        self.spam_dict_urls_and_ids = {}
        self.file = file

        self.client = TelegramClient(session_name, api_id, api_hash)
        self.client.start()

    async def run_case(self):
        await self.get_spam_ids()
        await self.save_spam_message()

    async def save_spam_message(self):
        for chat_url in self.spam_dict_urls_and_ids.keys():
            await self.iteration_messages_from_chat(chat_url)

    async def get_spam_ids(self):
        async for message in self.client.iter_messages(self.chat):
            if await self.processing_spam_message(message) is False:
                break
            else:
                continue

    def write_spam_message_in_file(self, message_text):
        with open(f'../../data/{self.file}', 'a') as file:
            file.write(message_text + '\n')

    async def processing_spam_message(self, message):
        logger.debug(f'Функция используется под сообщением: {message.text}')
        if re.search(r'https://t\.me/', message.text):
            id_message = int(message.text.split('/')[-1])
            chat_url = re.findall(r'https://t\.me/.*?/', message.text)[0]
            self.save_spam_ids(chat_url, id_message)
        elif message.text == 'flag TRUE':
            return False
        else:
            self.write_spam_message_in_file(message.text.replace('\n', ' '))
        await self.delete_message(message.id)

    async def iteration_messages_from_chat(self, chat_url):
        messages_from_chat = await self.client.get_messages(chat_url, limit=10000)
        for message in messages_from_chat:
            if message.id in self.spam_dict_urls_and_ids[chat_url]:
                self.write_spam_message_in_file(message.message.replace('\n', ' '))
                self.spam_dict_urls_and_ids[chat_url].remove(message.id)
            else:
                continue

    def save_spam_ids(self, chat_url, spam_id):
        if chat_url not in self.spam_dict_urls_and_ids.keys():
            self.spam_dict_urls_and_ids[chat_url] = []
        self.spam_dict_urls_and_ids[chat_url].append(spam_id)
        logger.info(f'Промежуточный словарь ids: {self.spam_dict_urls_and_ids}')

    async def delete_message(self, message_id):
        await self.client.delete_messages(self.chat, message_id)