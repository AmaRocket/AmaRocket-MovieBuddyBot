from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _, bot, dp


def get_markup():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Russian"), callback_data="lang_ru")],
            [InlineKeyboardButton(text=_("English"), callback_data="lang_en")],
            [InlineKeyboardButton(text=_("Ukraine"), callback_data="lang_uk")],
        ]
    )
