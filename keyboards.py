from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from typing import Union


def create_markup(words: list[Union[KeyboardButton, str]], count: int = 3, onetime: bool = True) -> ReplyKeyboardMarkup:
    def split_for_count(elements: list, ct: int):
        return [elements[i:i + ct] for i in range(0, len(elements), ct)]

    def generate_buttons(elements: list):
        for elem in elements:
            if type(elem) is not KeyboardButton:
                yield KeyboardButton(text=elem)
            else:
                yield elem

    words = split_for_count(list(generate_buttons(words)), count)
    return ReplyKeyboardMarkup(
        keyboard=words,
        resize_keyboard=True,
        selective=True,
        one_time_keyboard=onetime
    )