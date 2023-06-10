import re

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

object_type_names = {
    "su35": "Винищувач СУ-35",
    "shahed": "Дрон Шахед-138",
    "mi24": "Гвинтокрил МІ-24",
    "cal": "Ракета Калібр",
    "orlan10": "Дрон Орлан-10",
    "djimavic": "Дрон DJI Mavic",
    "iskander": "Ракета Іскандер"
}


def get_key_by_value(value):
    for key, val in object_type_names.items():
        if val == value:
            return key
    return None


test_bucket = 'airborne-object-detection-test'
data_bucket = 'airborne-object-detection-data'


def get_object_names():
    return list(object_type_names.values())


def map_object_type_to_name(object_type):
    return object_type_names.get(object_type, "Unknown Type")


def generate_object_type_keyboard():
    keyboard = [
        [InlineKeyboardButton(object_type_names[key], callback_data=key)]
        for key in object_type_names
    ]
    return InlineKeyboardMarkup(keyboard)


def is_valid_phone_number(phone_number):
    if re.match("^(\\+)?380(\(\d{2}\)|\d{2})\d{7}$", phone_number):
        return True
    else:
        return False
