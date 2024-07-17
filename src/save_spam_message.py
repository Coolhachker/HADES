from telethon import TelegramClient
import re
import asyncio
from typing import Union, List


class SaverSpamMessages:
    def __init__(self, api_id, api_hash, session_name):
        self.chat = 'https://t.me/kefvkeve'
        self.spam_list_ids: List[Union[str, int]] = []
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.client.start()

    async def get_spam_message(self):
        async for message in self.client.iter_messages(self.chat):
            if await self.processing_spam_message(message) is False:
                break
            else:
                continue

    async def get_spam_ids(self):
        pass

    @classmethod
    def write_spam_message_in_file(cls, message_text):
        with open('spam_messages.txt', 'a') as file:
            file.write(message_text + '\n')

    async def processing_spam_message(self, message):
        if re.search(r'https://t\.me/', message.text):
            id_message = int(message.text.split('/')[-1])
            chat_url = re.findall(r'https://t\.me/.*?/', message.text)[0]
            await self.iteration_messages_from_chat(id_message, chat_url)
        elif message.text == 'flag TRUE':
            return False
        else:
            self.write_spam_message_in_file(message.text)

    async def iteration_messages_from_chat(self, id_message, chat_url):
        async for message_from_chat in self.client.iter_messages(chat_url):
            if message_from_chat.id == id_message:
                self.write_spam_message_in_file(message_from_chat.text)
                break
            else:
                continue

    def save_spam_ids(self, spam_id):
        self.spam_list_ids.append(spam_id)


if __name__ == '__main__':
    data = {'api_id': 19567654, 'api_hash': '7ec7d44a4889e041dd667dc760b323e1', 'session_name': 'session'}
    saver_spam_messages = SaverSpamMessages(**data)
    asyncio.get_event_loop().run_until_complete(saver_spam_messages.get_spam_message())