import datetime
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from tmdb_v3_api import TheMovie
from database.db import DBCommands, Criteria
from keyboards.default import vote_average

from keyboards.inline.choise_buttons import menu_, genres_keyboard, total_keyboard, result_keyboard
from loader import dp, bot

import asyncio
from aiogram.types import ChatActions

from message_output.message_output import MessageText
from states.criteria import FormCriteria

# ================ DATA BASE SETTINGS =================================================================================

db = DBCommands()


# =====================================================================================================================

@dp.callback_query_handler(Text(startswith='criteria'))
async def choose_option(callback: types.CallbackQuery):
    """

    :param callback:
    :return: genres keyboard
    """
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await FormCriteria.genre.set()
    await callback.message.reply('Choose Genre:',
                                 reply_markup=genres_keyboard())
    await callback.answer()


@dp.callback_query_handler(state=FormCriteria.genre)
async def process_genre(callback: types.CallbackQuery, state: FSMContext):
    """
    Process genre edit
    """
    async with state.proxy() as data:
        data['genre'] = callback.data

    genre = int(callback.data)
    item = Criteria()
    item.genre = genre
    await state.update_data(item=item)

    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await FormCriteria.next()
    await callback.message.answer('Enter Vote Average: ',
                                  reply_markup=vote_average)


@dp.message_handler(lambda message: not message.text.isdigit(), state=FormCriteria.voteaverage)
async def process_vote_average_invalid(message: types.Message):
    """
    if vote average is invalid
    """
    return await message.answer('Vote average may be a number. \n Rate it! (digits only)')


@dp.message_handler(lambda message: message.text.isdigit(), state=FormCriteria.voteaverage)
async def process_voteaverage(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return: input year message
    """
    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    # Update state and data
    await FormCriteria.next()
    await state.update_data(voteaverage=int(message.text))

    data = await state.get_data()
    item: Criteria = data.get('item')
    voteaverage = int(message.text)
    item.vote_average = voteaverage
    await state.update_data(item=item)

    await message.answer("What is the Year?", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: not message.text.isdigit(), state=FormCriteria.year)
async def process_year_invalid(message: types.Message):
    """
    if year is invalid
    """
    return await message.reply('Year may be a number. \n Example: 1999 (digits only)')


@dp.message_handler(state=FormCriteria.year)
async def process_year(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return: confirmation request search by criteria
    """
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['year'] = message.text

        data = await state.get_data()
        item: Criteria = data.get('item')
        year = int(message.text)
        item.year = year
        item.users_id = user_id
        item.time = datetime.datetime.now()

        await item.create()

        await state.reset_state()

        # For "typing" message in top console
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.3)

        item.year = item.year
        item.vote_average = item.vote_average
        item.genre = item.genre

        text = (f'<b> Genre ID: </b>{item.genre}\n'
                f'<b> Vote Average </b>{item.vote_average}\n'
                f'<b> Year </b>{item.year}\n'
                )

        img = open('../media/futurama-fry-gif-wallpaper-futurama-1668529063.jpg', 'rb')
        await bot.send_photo(message.chat.id, photo=img)
        await sleep(1)

        await message.answer(text=text, reply_markup=total_keyboard())


@dp.callback_query_handler(Text(startswith='total'))
async def total(callback: types.CallbackQuery):
    """

    :param callback:
    :return: list of movies by criteria
    """
    try:
        first = int(callback['data'].replace('total_', ''))

        criteria = await db.show_criteria()

        i = str()
        for index in criteria:
            i = index

        genre = i.genre
        voteaverage = i.vote_average
        year = i.year

        movie_list = TheMovie().discover.discover_movies({
            'sort_by': 'popularity.desc',
            'vote_count.gte': '',
            'with_genres': f'{genre}',
            'vote_average.gte': f'{voteaverage}',
            'primary_release_year': f'{year}'
        })

        text_value = MessageText.message(movie_list, first)

        original_name = MessageText.original_title(text_value)
        movie_id = MessageText.movie_id(text_value)

        # For "typing" message in top console
        await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.25)

        await callback.message.edit_text(text=text_value)
        await callback.message.edit_reply_markup(
            reply_markup=result_keyboard(first, len(movie_list), original_name, movie_id))
    except IndexError:
        await callback.message.reply('Sorry. No Results', reply_markup=menu_())

# =====================================================================================================================
