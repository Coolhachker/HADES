from keras.layers import TextVectorization
from tensorflow._api.v2.strings import lower, regex_replace
from tensorflow import expand_dims
import re
import string
from logging import getLogger
logger = getLogger()


class VectorizationData:
    def __init__(self, dataframe_from_numpy):
        self.dataframe_from_numpy = dataframe_from_numpy
        self.numpy_messages_without_markers = [str(obj[0]) for obj in self.dataframe_from_numpy]

        self.sequences_length = 350
        self.vectorization_layer = self.set_vectorization_layer()
        self.adapt_layer()

    def chars_to_ids(self, text):
        text = expand_dims(text, -1)
        return self.vectorization_layer(text)

    @classmethod
    def set_label_to_sequences_spam(cls, tensor):
        return tensor, 0

    @classmethod
    def set_label_to_sequences_simple(cls, tensor):
        return tensor, 1

    @classmethod
    def standardize(cls, text):
        lower_case = lower(text)
        return regex_replace(lower_case, "[%s]" % re.escape(string.punctuation), '')

    def set_vectorization_layer(self):
        return TextVectorization(
            standardize=self.standardize,
            output_mode="int",
            max_tokens=100000,
            output_sequence_length=self.sequences_length,
        )

    def adapt_layer(self):
        self.vectorization_layer.adapt(self.numpy_messages_without_markers)
        logger.info(f'Токены в слое TextVectorization: {self.vectorization_layer.get_vocabulary()}')

    def __call__(self, *args, **kwargs):
        return self.vectorization_layer