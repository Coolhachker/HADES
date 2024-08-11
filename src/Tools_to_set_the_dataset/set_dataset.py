from tensorflow.python.data import Dataset
from src.Tools_to_set_the_dataset.vectorization_data import VectorizationData
import logging
from src.set_logger import ColoredFormat
from tensorflow.python.data.experimental import AUTOTUNE
from tensorflow import constant
file_handler = logging.FileHandler('../../logs/set_dataset.log', mode='w')
file_handler.setFormatter(ColoredFormat())

logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger()


class HadesDataset:
    def __init__(self, numpy_dataframe_with_spam_and_ham_messages):
        self.vectorization_layer = VectorizationData(numpy_dataframe_with_spam_and_ham_messages)
        self.bath_size = 30

        self.numpy_dataframe_with_spam_and_ham_messages_for_train = [(self.vectorization_layer.chars_to_ids(str(obj[0]))) for obj in numpy_dataframe_with_spam_and_ham_messages[:1100]]
        self.numpy_dataframe_with_spam_and_ham_messages_for_validation = [self.vectorization_layer.chars_to_ids(str(obj[0])) for obj in numpy_dataframe_with_spam_and_ham_messages[-300:]]
        self.numpy_dataframe_with_spam_and_ham_messages_for_test = [self.vectorization_layer.chars_to_ids(str(obj[0])) for obj in numpy_dataframe_with_spam_and_ham_messages[1100:1200]]

        self.numpy_dataframe_with_spam_and_ham_messages_for_train_labels = [constant(int(obj[1]), shape=(1, 1)) for obj in numpy_dataframe_with_spam_and_ham_messages[:1100]]
        self.numpy_dataframe_with_spam_and_ham_messages_for_validation_labels = [constant(int(obj[1]), shape=(1, 1)) for obj in numpy_dataframe_with_spam_and_ham_messages[-300:]]
        self.numpy_dataframe_with_spam_and_ham_messages_for_test_labels = [constant(int(obj[1]), shape=(1, 1)) for obj in numpy_dataframe_with_spam_and_ham_messages[1100:1200]]

        self.HadesDataset = self.set_train_dataset()
        self.HadesDatasetValid = self.set_valid_dataset()
        self.HadesDatasetTest = self.set_test_dataset()
        self.settings_dataset(self.HadesDataset)
        self.settings_dataset(self.HadesDatasetValid)

    def set_train_dataset(self):
        logger.info('Постановка датасета')
        return Dataset.from_tensor_slices((self.numpy_dataframe_with_spam_and_ham_messages_for_train, self.numpy_dataframe_with_spam_and_ham_messages_for_train_labels))

    def set_valid_dataset(self):
        logger.info('Постановка датасета для валидации данных')
        return Dataset.from_tensor_slices((self.numpy_dataframe_with_spam_and_ham_messages_for_validation, self.numpy_dataframe_with_spam_and_ham_messages_for_validation_labels))

    def set_test_dataset(self):
        logger.info('Постановка датасета теста модели')
        return Dataset.from_tensor_slices((self.numpy_dataframe_with_spam_and_ham_messages_for_test, self.numpy_dataframe_with_spam_and_ham_messages_for_test_labels))

    @staticmethod
    def settings_dataset(dataset):
        logger.info('Настройка датасета')
        dataset.cache().prefetch(AUTOTUNE)

    def vectorize_dataset(self, dataset):
        dataset.map(self.vectorization_layer.chars_to_ids)
