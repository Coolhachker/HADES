from csv import writer
import logging
from dotenv import dotenv_values, set_key
import os
logger = logging.getLogger()


class CSVConverterFromTxt:
    def __init__(self, file_name, file_name_csv):
        self.file_name = file_name
        self.file_name_csv = file_name_csv
        self.list_of_messages: list = []
        count_of_messages = int(dotenv_values('count_of_messages.env').get('COUNT'))
        self.buffer_file()
        logger.info(len(self.list_of_messages))
        set_key('count_of_messages.env', 'COUNT', str(count_of_messages+len(self.list_of_messages)))

    def buffer_file(self):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if self.list_of_messages.count(line.replace('\n', ' ')) == 1:
                    continue
                else:
                    self.list_of_messages.append(line.replace('\n', ' '))
        with open('../../data/spam_messages_buffer.txt', 'a') as file:
            for line in self.list_of_messages:
                file.write(line+'\n')

    def convert_to_csv(self):
        with open('../../data/spam_messages_buffer.txt', 'r') as file:
            lines = file.readlines()
            with open(f'../../data/{self.file_name_csv}', 'a', newline='', encoding='utf-8-sig') as csv_file:
                csv_writer = writer(csv_file, delimiter=';')
                for line in lines:
                    csv_writer.writerow(line.split('\n'))
        with open(self.file_name, 'w'):
            pass
        with open('../../data/spam_messages_buffer.txt', 'w'):
            pass