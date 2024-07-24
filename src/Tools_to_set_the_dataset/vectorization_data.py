from keras.layers import TextVectorization
from tensorflow._api.v2.strings import lower, regex_replace
from tensorflow import expand_dims
import re
import string


class VectorizationData:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.sequences_length = 350
        self.vectorization_layer = self.set_vectorization_layer()
        self.adapt_layer()

    def chars_to_ids(self, text, label):
        text = expand_dims(text, -1)
        return self.vectorization_layer(text), label

    @classmethod
    def standardize(cls, text):
        lower_case = lower(text)
        return regex_replace(lower_case, "[%s]" % re.escape(string.punctuation))

    def set_vectorization_layer(self):
        return TextVectorization(
            standardize=self.standardize,
            output_mode="int",
            max_tokens=self.sequences_length
        )

    def adapt_layer(self):
        with open(self.path_to_file) as file:
            for string_ in file:
                self.vectorization_layer.adapt(string_)

    @property
    def return_layer(self):
        return self.vectorization_layer

    def __new__(cls, *args, **kwargs):
        return cls.return_layer