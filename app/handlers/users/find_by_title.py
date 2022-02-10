import asyncio
import datetime
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatActions

from database.db import DBCommands, Title
from keyboards.inline.choise_buttons import (menu_, title_keyboard,
                                             title_movie_buttons)
from loader import _, bot, dp
from message_output.message_output import MessageText
from states.criteria import FormCriteria
from tmdb_v3_api import get_api_for_context

# ================ DATA BASE SETTINGS =================================================================================

db = DBCommands()


# =====================================================================================================================


@dp.callback_query_handler(Text(startswith="title"))
async def choose_option(callback: types.CallbackQuery):
    """

    :param callback:
    :return: request for searching movie by title
    """
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.25)

    await FormCriteria.title.set()
    await callback.message.answer(_("Enter Title Of Film:"))
    await callback.answer()


@dp.message_handler(state=FormCriteria.title)
async def find_by_title(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return: confirmation request with movie title
    """

    async with state.proxy() as data:
        data["title"] = message.text

        item = Title()

        user_id = types.User.get_current()
        item.title = data["title"]
        item.users_id = user_id
        item.time = datetime.datetime.now()
        await state.update_data(item=item)

        data = await state.get_data()
        item: Title = data.get("item")

        await item.create()
        img = open("../media/futurama-fry-gif-wallpaper-futurama-1668529063.jpg", "rb")
        await bot.send_photo(message.chat.id, photo=img)
        await sleep(1)
        await message.reply(
            _("{item}").format(item=item.title), reply_markup=title_keyboard()
        )

        await state.reset_state()


@dp.callback_query_handler(Text(startswith="find"))
async def title(callback: types.CallbackQuery):
    """

    :param callback:
    :return: list of movies by title
    """
    try:
        first = int(callback["data"].replace("find_", ""))

        movie_title = await db.show_title()

        i = str()
        for index in movie_title:
            i = index

        name = i.title

        tmdb_with_language = await get_api_for_context(callback.message.chat.id)

        movie_list = tmdb_with_language.movie.search(name)

        message = MessageText(movie_list[first])
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
            reply_markup=title_movie_buttons(
                first, len(movie_list), message.original_title, message.movie_id
            )
        )
    except IndexError:
        await callback.answer()
        await callback.message.reply(_("Sorry. No Results"), reply_markup=menu_())


# =====================================================================================================================
