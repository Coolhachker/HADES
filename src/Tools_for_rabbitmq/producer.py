import pika
from typing import Any, Optional, Union
import re
from src.Tools_for_rabbitmq.Queue import Queue
from pika import exceptions
from src.Configs.Hosts import Hosts
from src.Configs.Exceptions import ResponseExceptions


class Producer:
    def __init__(self, host):
        self.parameters = pika.ConnectionParameters(heartbeat=60, host=host)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

        self.exchange = ''
        self.queue = Queue.spam_queue
        self.callback_queue = Queue.spam_queue_callback

        self.declare_queue()
        self.consume_the_response()

        self.response: Optional[str] = None
        self.info_response: Union[str, None] = None

    def declare_queue(self):
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_declare(queue=self.callback_queue, durable=True)

    def publish(self, message: Any, properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent), queue=None, callback_queue=None):
        properties = pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent, reply_to=self.callback_queue)
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.queue if queue is None else queue,
                body=message.encode(),
                properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent, reply_to=self.callback_queue)
            )

            while self.response is None:
                self.connection.process_data_events(time_limit=60)
            else:
                response = self.response
                self.response = None
                return response
        except exceptions.ChannelWrongStateError:
            self.reconnect()
            self.publish(message=message, properties=properties, queue=queue)

    def close_connection(self):
        self.channel.close()

    def consume_the_response(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, channel, method, properties, body: bytes):
        if re.search(r'ERROR', body.decode()):
            raise ResponseExceptions.WronglyResponse(f'Ошибка: {body.decode()}')
        else:
            self.response = body.decode()

    def reconnect(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()


producer = Producer(Hosts.rabbitmq)
