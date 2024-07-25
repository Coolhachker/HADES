from keras.callbacks import ModelCheckpoint, EarlyStopping
from src.Tools_to_set_the_dataset.set_dataset import SpamDataset
from src.Tools_for_compile_the_model.set_model import Hades
from keras.losses import BinaryCrossentropy
from keras.metrics import BinaryAccuracy
import os


class Education:
    def __init__(self):
        self.dataset_object = SpamDataset('../../data/spam_messages.txt', '')
        self.dataset = self.dataset_object.HadesDataset
        vocab_size = len(self.dataset_object.vectorization_layer.vectorization_layer.get_vocabulary())
        embedding_dim = 16

        self.model = Hades(embedding_dim=embedding_dim, max_features=vocab_size)
        self.compile_model()
        self.checkpoint_callback = self.create_checkpoints()
        self.early_stopping_callback = self.create_early_stopping()
        self.epoch = 10

    def compile_model(self):
        self.model.compile(
            optimizer='adam',
            loss=BinaryCrossentropy(from_logits=True),
            metrics=BinaryAccuracy(threshold=0.0)
        )

    @staticmethod
    def create_checkpoints():
        """
        Функция создает checkpoints для сохранения модели на время обучения

        :return:
        """
        checkpoints_prefix = os.path.join('checkpoints', 'ckpt_{epoch}')
        return ModelCheckpoint(
            filepath=checkpoints_prefix,
            save_weights_only=True
        )

    @staticmethod
    def create_early_stopping():
        """
        Функция создает early stopping для остановки обучения модели

        :return:
        """
        return EarlyStopping(
            monitor='val_loss',
            patience=1,
            restore_best_weights=True
        )

    def fit_model(self):
        self.model.fit(
            self.dataset,
            epochs=self.epoch,
            callbacks=[self.checkpoint_callback, self.early_stopping_callback]
        )


if __name__ == '__main__':
    model = Education()
    model.fit_model()
