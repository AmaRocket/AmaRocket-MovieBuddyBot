import re

from aiogram import types
from aiogram.dispatcher.filters import Text

from TEST_TMDB_PIPY import TheMovie

from keyboards.inline.choise_buttons import popular_movie_buttons
from loader import dp, bot

import asyncio
from aiogram.types import ChatActions

# ================ POPULAR ============================================================================================
from message_output.message_output import MessageText


@dp.callback_query_handler(Text(startswith='popular'))
async def poppular_by(callback: types.CallbackQuery):
    """

    :param callback:
    :return: list with popular movies from tmdbv3api
    """
    movie_list = TheMovie().movie.popular()

    first = int(callback['data'].replace('popular_', ''))

    # Message List
    text_value = MessageText().message(movie_list, first)

    original_name = ((re.findall(r'Movie: (.+)', text_value))[-1])
    print(original_name)
    movie_id = ((re.findall(r'ID: (\d+)', text_value))[-1])
    print(movie_id)

    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await callback.message.edit_text(text=text_value)
    await callback.message.edit_reply_markup(
        reply_markup=popular_movie_buttons(first, len(movie_list), original_name, movie_id))

# =====================================================================================================================
