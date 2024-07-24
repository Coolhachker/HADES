from tensorflow.python.data import Dataset
from src.Tools_to_set_the_dataset.vectorization_data import VectorizationData


class SpamDataset:
    def __init__(self, path_to_file):
        self.vectorization_layer = VectorizationData(path_to_file)

    def set_spam_dataset(self):
        pass
