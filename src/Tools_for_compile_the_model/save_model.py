from tensorflow import saved_model
from classification_model_export import HadesClassification
from typing import List
from tensorflow import constant


def save(text: List[str]):
    __HADES__ = HadesClassification()
    __HADES__.classify(constant(text))
    saved_model.save(__HADES__, 'HADES')


if __name__ == '__main__':
    save(['абоба'])