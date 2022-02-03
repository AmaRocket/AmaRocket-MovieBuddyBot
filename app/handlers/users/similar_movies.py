import re

from aiogram import types
from aiogram.dispatcher.filters import Text

from TEST_TMDB_PIPY import TheMovie

from keyboards.inline.choise_buttons import similar_movie_keyboard, menu_
from loader import dp, bot

import asyncio
from aiogram.types import ChatActions


# ================ SIMILAR ============================================================================================

@dp.callback_query_handler(Text(startswith='similar'))
async def movie_like_this(callback: types.CallbackQuery):
    """

    :param callback:
    :return: similar movies by move_id
    """
    try:

        # await state.finish()
        message = callback.message.text

        movie_id = (re.findall(r'ID: (\d+)', message))
        m_id = movie_id[-1]

        movie_list = TheMovie().movie.recommendations(m_id)
        first = int(callback['data'].replace('similar_', ''))
        print(first)
        print(type(first))

        id = movie_list[first]['id']
        genre_ids = movie_list[first]['genre_ids']
        original_name = movie_list[first]['title']
        original_language = movie_list[first]['original_language']
        overview = movie_list[first]['overview']
        vote_average = movie_list[first]['vote_average']
        vote_count = movie_list[first]['vote_count']
        release_date = movie_list[first]['release_date']
        popularity = movie_list[first]['popularity']
        poster_path = movie_list[first]['poster_path']

        text_value = f' ID: {id}\n Movie: {original_name}\n Release date: {release_date}\n Genre id: {genre_ids}\n' \
                     f' Original languare {original_language}\n Overwiew: {overview}\n Voteaverage: {vote_average}\n' \
                     f' Vote count: {vote_count}\n Popularity: {popularity}\n Genre id: {genre_ids}\n ' \
                     f' Poster path: https://image.tmdb.org/t/p/original{poster_path}\n' \
                     f'---------------------------------------------------------------------------------------------'

        # For "typing" message in top console
        await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(1)

        await callback.message.edit_text(text=text_value)
        await callback.message.edit_reply_markup(
            reply_markup=similar_movie_keyboard(first, len(movie_list), original_name, id))
    except IndexError as ex:
        await callback.message.reply('Sorry. No Results', reply_markup=menu_())

# =====================================================================================================================
