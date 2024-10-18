import typing
from functools import lru_cache
from mysql.connector import connect
import mysql
import logging
from src.Configs.Hosts import Hosts
logger = logging.getLogger()


class MysqlDB:
    def __init__(self):
        self.connection, self.cursor = self.connect_to_db()
        self.create_table()

    def connect_to_db(self):
        try:
            connection = connect(
                host=Hosts.mysql_db,
                user='root',
                password='root1234567890',
                auth_plugin='mysql_native_password',
                database='ANTI-SPAM-DB'
            )
            logger.info('Успешное подключение')
            return connection, connection.cursor(buffered=True)
        except mysql.connector.errors.ProgrammingError:
            connection = connect(
                host=Hosts.mysql_db,
                user='root',
                password='root1234567890',
                auth_plugin='mysql_native_password',
            )
            cursor = connection.cursor()
            cursor.execute('CREATE DATABASE ANTI-SPAM-DB')
            connection.commit()
            self.connect_to_db()

    def create_table(self):
        # self.cursor.execute('DROP TABLE trusted_users')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS admins(user_nickname TEXT, chat_id_of_admin INT UNSIGNED, chat_id INT UNSIGNED)')
        self.connection.commit()

    @lru_cache(maxsize=128)
    def add_entry_in_admins(self, chat_id_of_user: int, chat_id: int, username: str):
        self.cursor.executemany("""INSERT INTO admins(username, chat_id_of_admin, chat_id) VALUES(%s, %s, %s)""", [(username, chat_id_of_user, chat_id)])
        self.connection.commit()

    def get_chat_id_of_admin(self, chat_id: int) -> typing.List[str]:
        self.cursor.execute(f'SELECT chat_id_of_admin FROM admins WHERE chat_id = {chat_id}')
        result = self.cursor.fetchall()
        return result[0][0]

    def delete_admin_from_db(self, chat_id_of_admin: int):
        self.cursor.execute(f"""DELETE FROM admins WHERE chat_id_of_admin = {chat_id_of_admin} """)
        self.connection.commit()

    def reconnect(self):
        self.connection, self.cursor = self.connect_to_db()
        self.create_table()


client_mysqldb = MysqlDB()


