from keras.callbacks import ModelCheckpoint, EarlyStopping
from src.Tools_to_set_the_dataset.set_dataset import HadesDataset
from src.Tools_for_compile_the_model.set_model import Hades
from keras.losses import BinaryCrossentropy
from keras.metrics import BinaryAccuracy
from src.Tools_to_set_the_dataset.set_dataset_from_csv import set_dataframe_from_csv
from keras.models import Sequential
from keras.layers import Activation
import os


class Education:
    def __init__(self):
        self.dataset_object = HadesDataset(set_dataframe_from_csv('../../data/spam_messages.csv', '../../data/ham_messages.csv'))
        self.dataset = self.dataset_object.HadesDataset
        self.dataset_for_valid = self.dataset_object.HadesDatasetValid
        self.dataset_for_test = self.dataset_object.HadesDatasetTest
        vocab_size = len(self.dataset_object.vectorization_layer.vectorization_layer.get_vocabulary())
        embedding_dim = 16

        self.model = Hades(embedding_dim=embedding_dim, max_features=vocab_size)
        self.compile_model()
        self.checkpoint_callback = self.create_checkpoints()
        self.early_stopping_callback = self.create_early_stopping()
        self.epoch = 30

        self.fit_model()
        self.hades = self.export_model()

    def compile_model(self):
        self.model.compile(
            optimizer='adam',
            loss=BinaryCrossentropy(from_logits=False),
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
            callbacks=[self.checkpoint_callback, self.early_stopping_callback],
            validation_data=self.dataset_for_valid
        )

    def check_model(self):
        print(self.model.predict(self.dataset_object.vectorization_layer.chars_to_ids('Зарабатываем удаленно от десяти тысяч рублей в неделю. За  подробностями пиши в личные сообщения'))[0][0] * 10)

    def export_model(self):
        hades = Sequential([
            self.dataset_object.vectorization_layer.vectorization_layer,
            self.model
        ])
        hades.compile(
            loss=BinaryCrossentropy(),
            optimizer='adam',
            metrics=['accuracy']
        )

        return hades

    def __call__(self, text, *args, **kwargs):
        return self.hades.predict(text)


if __name__ == '__main__':
    model = Education()
    result = model(['Не сторож, а дегустатор. По виду'])
    print(result)
