
from aiogram import types
from aiogram.dispatcher.filters import Text

from TEST_TMDB_PIPY import TheMovie

from keyboards.inline.choise_buttons import popular_movie_buttons
from loader import dp, bot

import asyncio
from aiogram.types import ChatActions



# ================ POPULAR ============================================================================================


@dp.callback_query_handler(Text(startswith='popular'))
async def poppular_by(callback: types.CallbackQuery):
    """

    :param callback:
    :return: list with popular movies from tmdbv3api
    """
    popular_list = TheMovie().movie.popular()

    first = int(callback['data'].replace('popular_', ''))

    # Message List
    id = popular_list[first]['id']
    genre_ids = popular_list[first]['genre_ids']
    original_name = popular_list[first]['title']
    original_language = popular_list[first]['original_language']
    overview = popular_list[first]['overview']
    vote_average = popular_list[first]['vote_average']
    vote_count = popular_list[first]['vote_count']
    release_date = popular_list[first]['release_date']
    popularity = popular_list[first]['popularity']
    poster_path = popular_list[first]['poster_path']

    text_value = f' ID: {id}\n Movie: {original_name}\n Release date: {release_date}\n Genre id: {genre_ids}\n' \
                 f' Original languare {original_language}\n Overwiew: {overview}\n Voteaverage: {vote_average}\n' \
                 f' Vote count: {vote_count}\n Popularity: {popularity}\n Genre id: {genre_ids}\n ' \
                 f' Poster path: https://image.tmdb.org/t/p/original{poster_path}\n' \
                 f'------------------------------------------------------------------------------------------'

    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await callback.message.edit_text(text=text_value)
    await callback.message.edit_reply_markup(
        reply_markup=popular_movie_buttons(first, len(popular_list), original_name, id))


# =====================================================================================================================