from tensorflow.python.data import Dataset
from src.Tools_to_set_the_dataset.vectorization_data import VectorizationData
import logging
from src.set_logger import ColoredFormat
from tensorflow.python.data.experimental import AUTOTUNE
file_handler = logging.FileHandler('../../logs/set_dataset.log', mode='w')
file_handler.setFormatter(ColoredFormat())

logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger()


class SpamDataset:
    def __init__(self, path_to_file_with_spam_messages, path_to_file_with_simple_messages):
        self.vectorization_layer = VectorizationData(path_to_file_with_spam_messages)
        self.path_to_file_with_simple_messages = path_to_file_with_simple_messages
        self.path_to_file_with_spam_messages = path_to_file_with_spam_messages
        self.bath_size = 30
        self.Dataset_from_spam_messages = self.set_spam_dataset()
        self.set_label_to_spam(self.Dataset_from_spam_messages)
        self.setting_spam_dataset()

    def set_spam_dataset(self):
        list_with_tensors: list = []
        with open(self.path_to_file_with_spam_messages, 'r') as file:
            for string in file:
                list_with_tensors.append(self.vectorization_layer.chars_to_ids(string))
                logging.debug(f'Размерность тензора: {self.vectorization_layer.chars_to_ids(string).shape} ')
        return Dataset.from_tensor_slices(list_with_tensors)

    def set_label_to_spam(self, dataset):
        dataset.map(self.vectorization_layer.set_label_to_sequences_spam)

    def setting_spam_dataset(self):
        self.Dataset_from_spam_messages.cache().prefetch(AUTOTUNE)
