from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# =====================================================================================================================

vote_average = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=str(i)) for i in range(1, 10)],
        [KeyboardButton(text="Cancel")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# =====================================================================================================================

totalkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Finish")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# =====================================================================================================================
