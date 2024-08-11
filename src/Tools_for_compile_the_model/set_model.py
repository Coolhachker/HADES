from keras.models import Model
from keras.layers import Embedding, GlobalAveragePooling1D, Dropout, Dense
from tensorflow import GradientTape


class Hades(Model):
    def __init__(self, embedding_dim, max_features):
        super().__init__(self)

        self.embedding = Embedding(max_features+1, embedding_dim)
        # self.dropout = Dropout(0.1)
        self.pooling = GlobalAveragePooling1D()
        # self.dropout = Dropout(0.1)
        self.dense = Dense(1, activation='sigmoid')

    def call(self, inputs, training=None, mask=None):
        x = inputs
        x = self.embedding(x)
        # x = self.dropout(x, training=training)
        x = self.pooling(x)
        # x = self.dropout(x, training=training)
        x = self.dense(x)
        return x

    def train_step(self, data):
        """
        Функция для кастомного обучения. В этом случае обучение на градиенте ошибок.

        :param data:
        :return:
        """
        inputs, target = data
        with GradientTape() as tape:
            predictions = self(inputs, training=True)
            loss = self.loss(target, predictions)

        grads = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))

        return {'loss': loss}