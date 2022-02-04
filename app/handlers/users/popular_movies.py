from aiogram import types
from aiogram.dispatcher.filters import Text

from TEST_TMDB_PIPY import TheMovie

from keyboards.inline.choise_buttons import popular_movie_buttons
from loader import dp, bot

import asyncio
from aiogram.types import ChatActions

from message_output.message_output import MessageText


# ================ POPULAR ============================================================================================


@dp.callback_query_handler(Text(startswith='popular'))
async def poppular_by(callback: types.CallbackQuery):
    """

    :param callback:
    :return: list with popular movies from tmdbv3api
    """
    movie_list = TheMovie().movie.popular()

    first = int(callback['data'].replace('popular_', ''))

    # Message List
    text_value = MessageText.message(movie_list, first)

    original_name = MessageText.original_title(text_value)
    movie_id = MessageText.movie_id(text_value)

    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await callback.message.edit_text(text=text_value)
    await callback.message.edit_reply_markup(
        reply_markup=popular_movie_buttons(first, len(movie_list), original_name, movie_id))

# =====================================================================================================================
