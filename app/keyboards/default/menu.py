from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType

# =====================================================================================================================

vote_average = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
)
for i in range(1, 10):
    vote_average.insert(KeyboardButton(text=i))
vote_average.add(KeyboardButton(text='Cancel'))

# =====================================================================================================================

totalkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Finish')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# =====================================================================================================================
