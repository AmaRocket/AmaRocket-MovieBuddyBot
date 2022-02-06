import datetime
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from tmdb_v3_api import TheMovie
from database.db import Title, DBCommands

from keyboards.inline.choise_buttons import title_keyboard, title_movie_buttons, menu_
from loader import dp, bot

import asyncio
from aiogram.types import ChatActions

from states.criteria import FormCriteria

from message_output.message_output import MessageText

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
        img = open('../media/futurama-fry-gif-wallpaper-futurama-1668529063.jpg', 'rb')
        await bot.send_photo(message.chat.id, photo=img)
        await sleep(1)
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

        movie_title = await db.show_title()

        i = str()
        for index in movie_title:
            i = index

        name = i.title
        movie_list = TheMovie().movie.search(name)

        text_value = MessageText.message(movie_list, first)
        original_name = MessageText.original_title(text_value)
        movie_id = MessageText.movie_id(text_value)

        # For "typing" message in top console
        await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.5)

        await callback.message.edit_text(text=text_value)
        await callback.message.edit_reply_markup(
            reply_markup=title_movie_buttons(first, len(movie_list), original_name, movie_id))
    except IndexError:

        await callback.message.reply(text='Sorry. No Results', reply_markup=menu_())

# =====================================================================================================================
