from dataclasses import dataclass


@dataclass
class Hosts:
    mongodb: str = 'localhost'
    mysql_db: str = '172.15.235.2'
    rabbitmq: str = '172.15.235.7'