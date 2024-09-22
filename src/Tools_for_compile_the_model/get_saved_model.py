from typing import List
from tensorflow import saved_model
hades = saved_model.load('HADES')


def classify(text: List[str]):
    """
    Функция классификации сообщений
    :param text:
    :return: 0 - не спам, 1 - спам
    """
    result = hades.classify(text).numpy()[0][0] * 10
    print(result)
    return 0 if result <= 0.11 else 1