from typing import List
from tensorflow import saved_model
from numpy import argmax
hades = saved_model.load('/Users/egor/PycharmProjects/AntiSpamBot/src/Tools_for_compile_the_model/HADES')


def classify(text: List[str]) -> bool:
    result = hades.classify(text).numpy()[0][0] * 10
    if result >= 0.1:
        return True
    else:
        return False


if __name__ == '__main__':
    print(classify(['у меня были все провайдеры']))