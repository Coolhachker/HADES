from typing import List
from tensorflow import saved_model
from numpy import argmax
hades = saved_model.load('HADES')


def classify(text: List[str]):
    return hades.classify(text).numpy()[0][0]


if __name__ == '__main__':
    print(classify(['Кому нужна подработка в лс От вас 14+ лет и 1000-2000руб от вас на старте Не закладки ! Работа онлайн в телефоне или компьютер и т.д;']))