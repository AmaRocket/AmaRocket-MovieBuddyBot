import asyncio
import datetime
import re

import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatActions

from database.db import DBCommands, MyMovies
from keyboards.inline.choise_buttons import my_movies
from loader import _, bot, dp
from message_output.message_output import MessageText
from tmdb_v3_api import get_api_for_context

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
    await asyncio.sleep(0.25)

    try:
        first = int(callback["data"].replace("movie_list_", ""))

        data = await db.show_movies()

        movie = []
        for i in data:
            movie.append(i.movie_id)

        movie_id = movie  # Get movie id from db

        tmdb_with_language = await get_api_for_context(callback.message.chat.id)

        movie_list = tmdb_with_language.movie.details(movie_id[first])

        message = MessageText((movie_list))

        if message.movie_image is None:
            poster = "https://image.tmdb.org/t/p/original"
        else:
            poster = "https://image.tmdb.org/t/p/original" + message.movie_image

        # For "typing" message in top console
        await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.25)

        await callback.message.edit_text(
            _("{message} {poster}").format(message=message.message, poster=poster)
        )
        await callback.message.edit_reply_markup(
            reply_markup=my_movies(
                first, len(movie_id), message.original_title, message.movie_id
            )
        )
    except IndexError:
        await callback.answer(_("Your Movie List Is Empty"))
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

    movie_id = int((re.findall(r"#️⃣ ID:  (\d+)", data))[-1])

    user_id = int(types.User.get_current())

    item.users_id = user_id
    item.movie_id = movie_id
    item.time = datetime.datetime.now()
    item.data = data

    try:
        await item.create()
        await callback.answer(_("Added To Your MovieList"))
    except asyncpg.exceptions.UniqueViolationError:
        await callback.answer(_("This Movie Already In Your List"))


@dp.callback_query_handler(Text(startswith="delete_from_movie_list"))
async def drop_my_movie(callback: types.CallbackQuery):
    """

    :param callback:
    :return: delete item from MyMovies Table
    """
    item = MyMovies()

    data = callback.get_current().message.text

    user_id = int(types.User.get_current())
    movie_id = int((re.findall(r"#️⃣ ID: .(\d+)", data))[-1])

    item_id = await db.get_movie(movie_id)

    item.id = item_id.id
    item.users_id = user_id
    item.movie_id = movie_id

    item.time = datetime.datetime.now()
    item.data = data

    await item.delete()
    await callback.answer(_("Deleted From Your MovieList"))


# =====================================================================================================================
