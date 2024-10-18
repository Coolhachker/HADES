from dataclasses import dataclass


@dataclass
class Queue:
    spam_queue: str = 'spam_queue'
    spam_queue_callback: str = 'spam_queue_callback'
    ping_queue: str = 'ping_queue'