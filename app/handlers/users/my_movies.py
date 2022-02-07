import asyncio
import datetime
import re

import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatActions

from database.db import DBCommands, MyMovies
from keyboards.inline.choise_buttons import my_movies
from loader import bot, dp

# ================ DATA BASE SETTINGS =================================================================================


db = DBCommands()


# =====================================================================================================================

# ================ MY_MOVIES ==========================================================================================


@dp.callback_query_handler(Text(startswith="movie_list"))
async def movie_list(callback: types.CallbackQuery):
    """
    :param callback:
    :return: data from MyMovie Table
    """

    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.3)

    try:
        first = int(callback["data"].replace("movie_list_", ""))
        data = await db.show_movies()
        print(type(data))
        movie = []
        for i in data:
            movie.append(i.data)

        text = movie[first]  # Get message data from db

        original_name = (re.findall(r"Movie: (.+)", text))[-1]
        movie_id = (re.findall(r"ID: (\d+)", text))[-1]

        await callback.message.edit_text(text=text)
        await callback.message.edit_reply_markup(
            reply_markup=my_movies(first, len(movie), original_name, movie_id)
        )
    except IndexError:
        await callback.answer(text="Your Movie List Is Empty")

    await callback.answer()


@dp.callback_query_handler(Text(startswith="add_to_movie_list"))
async def add_to_movie_list(callback: types.CallbackQuery):
    """
    Function for add movie to db list
    :param callback:
    :return: add data in MyMovie Table
    """
    item = MyMovies()
    data = callback.get_current().message.text

    movie_id = int((re.findall(r"ID: (\d+)", data))[-1])

    title = str((re.findall(r"Movie: (.+)", data))[-1])

    user_id = int(types.User.get_current())

    item.users_id = user_id
    item.movie_id = movie_id
    item.title = title
    item.time = datetime.datetime.now()
    item.data = data

    try:
        await item.create()
        await callback.answer(text="Added To Your MovieList")
    except asyncpg.exceptions.UniqueViolationError:
        await callback.answer(text="This Movie Already In Your List")


@dp.callback_query_handler(Text(startswith="delete_from_movie_list"))
async def drop_my_movie(callback: types.CallbackQuery):
    """

    :param callback:
    :return: delete item from MyMovies Table
    """
    item = MyMovies()

    data = callback.get_current().message.text

    user_id = int(types.User.get_current())
    movie_id = int((re.findall(r"ID: (\d+)", data))[-1])
    title = (re.findall(r"Movie: (.+)", data))[-1]

    item_id = await db.get_movie(movie_id)

    item.id = item_id.id
    item.users_id = user_id
    item.movie_id = movie_id
    item.title = str(title[-1])
    item.time = datetime.datetime.now()
    item.data = data

    await item.delete()
    await callback.answer(text="Deleted From Your MovieList")

# =====================================================================================================================
