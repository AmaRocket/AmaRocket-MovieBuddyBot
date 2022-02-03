import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from TEST_TMDB_PIPY import TheMovie
from data_base.db import Title, DBCommands

from keyboards.inline.choise_buttons import title_keyboard, title_movie_buttons, menu_
from loader import dp, bot

import asyncio
from aiogram.types import ChatActions

from states.criteria import FormCriteria

# ================ DATA BASE SETTINGS =================================================================================

db = DBCommands()


# =====================================================================================================================


@dp.callback_query_handler(Text(startswith='title'))
async def choose_option(callback: types.CallbackQuery):
    """

    :param callback:
    :return: request for searching movie by title
    """
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await FormCriteria.title.set()
    await callback.message.answer('Enter Title Of Film:')
    await callback.answer()


@dp.message_handler(state=FormCriteria.title)
async def find_by_title(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return: confirmation request with movie title
    """

    async with state.proxy() as data:
        data['title'] = message.text

        item = Title()

        user_id = types.User.get_current()
        item.title = data['title']
        item.users_id = user_id
        item.time = datetime.datetime.now()
        await state.update_data(item=item)

        data = await state.get_data()
        item: Title = data.get('item')

        await item.create()

        await message.reply(text=item.title, reply_markup=title_keyboard())

        await state.reset_state()


@dp.callback_query_handler(Text(startswith='find'))
async def title(callback: types.CallbackQuery):
    """

    :param callback:
    :return: list of movies by title
    """
    try:
        first = int(callback['data'].replace('find_', ''))

        title = await db.show_title()

        i = str()
        for i in title:
            i = i

        name = i.title
        movie_list = TheMovie().movie.search(name)

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
                     f'------------------------------------------------------------------------------------------'

        # For "typing" message in top console
        await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.5)

        await callback.message.edit_text(text=text_value)
        await callback.message.edit_reply_markup(
            reply_markup=title_movie_buttons(first, len(movie_list), original_name, id))
    except IndexError:

        await callback.message.reply(text='Sorry. No Results', reply_markup=menu_())

# =====================================================================================================================
