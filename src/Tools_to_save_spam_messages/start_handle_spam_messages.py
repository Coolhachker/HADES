from handler_spam_messages import HandlerMessages
import asyncio


if __name__ == '__main__':
    data = {'api_id': 19567654, 'api_hash': '7ec7d44a4889e041dd667dc760b323e1', 'session_name': 'session'}
    handler = HandlerMessages(data, 'spam_messages.txt', 'spam_messages.csv')
    asyncio.get_event_loop().run_until_complete(handler.handle())
