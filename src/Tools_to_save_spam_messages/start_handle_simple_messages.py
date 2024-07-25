from src.Tools_to_save_spam_messages.handler_spam_messages import HandlerMessages
import asyncio


if __name__ == '__main__':
    data = {'api_id': 19567654, 'api_hash': '7ec7d44a4889e041dd667dc760b323e1', 'session_name': 'session'}
    handler = HandlerMessages(data, 'simple_messages.txt')
    asyncio.get_event_loop().run_until_complete(handler.handle())
