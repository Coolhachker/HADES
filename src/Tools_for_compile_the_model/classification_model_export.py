from keras.models import Model
from src.Tools_for_compile_the_model.train_model import Education
from tensorflow import function
from typing import List


class HadesClassification(Model):
    def __init__(self):
        super().__init__()
        self.hades = Education()
        self.hades_model = self.hades.model
        self.vectorization_layer = self.hades.dataset_object.vectorization_layer.vectorization_layer

    @function
    def classify(self, text: List[str]):
        predicted_result = self.hades_model(self.vectorization_layer(text))
        return predicted_result


