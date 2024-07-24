from keras.callbacks import ModelCheckpoint, EarlyStopping
from src.Tools_to_set_the_dataset.set_dataset import SpamDataset


class Education:
    def __init__(self):
        self.dataset = SpamDataset()