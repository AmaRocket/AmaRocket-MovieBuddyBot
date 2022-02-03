from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


vote_average = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1'),
            KeyboardButton(text='2'),
            KeyboardButton(text='3'),
            KeyboardButton(text='4'),
            KeyboardButton(text='5'),
            KeyboardButton(text='6'),
            KeyboardButton(text='7'),
            KeyboardButton(text='8'),
            KeyboardButton(text='9')
        ],
        [
            KeyboardButton(text='Cancel')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

totalkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Finish')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
