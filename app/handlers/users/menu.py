import logging

import aiogram.utils.markdown as md

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from TEST_TMDB_PIPY import popular_movie, find_by_name
from config import api_key, DB_URI

from keyboards.default import genres, vote_average
from keyboards.inline.choise_buttons import popular_movie_buttons, menu_, title_movie_buttons, total_keyboard, \
    result_keyboard, title_keyboard
from loader import dp, bot
from aiogram.types import Message, ParseMode

from aiogram.dispatcher.filters import Command, Text

import asyncio
from aiogram.types import ChatActions

import psycopg2

db_connection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_connection.cursor()


class FormTitle(StatesGroup):
    title = State()


class FormCriteria(StatesGroup):
    genre = State()
    voteaverage = State()
    year = State()


# Work!
@dp.message_handler(Command('start'))
async def start_menu(message: Message):
    id = message.from_user.id
    username = message.from_user.username

    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)

    await message.reply(f'Hello {username}🖖🏻 \nSelect Your Option From Menu👇🏻', reply_markup=menu_())

    db_object.execute(f'SELECT id FROM users WHERE id = {id}')
    result = db_object.fetchone()

    if not result:
        db_object.execute('INSERT INTO users (id, username, count_messages) VALUES (%s, %s, %s)',(id, username, 0))
        db_connection.commit()


# List Of Popular Movies
@dp.callback_query_handler(Text(startswith='popular'))
async def poppular_by(callback: types.CallbackQuery):
    popular_list = popular_movie()
    first = int(callback['data'].replace('popular_', ''))
    # Message List
    id = popular_list[first]['id']
    genre_ids = popular_list[first]['genre_ids']
    original_name = popular_list[first]['original_title']
    original_language = popular_list[first]['original_language']
    overview = popular_list[first]['overview']
    vote_average = popular_list[first]['vote_average']
    vote_count = popular_list[first]['vote_count']
    release_date = popular_list[first]['release_date']
    popularity = popular_list[first]['popularity']
    poster_path = popular_list[first]['poster_path']

    text_value = f' Movie: {original_name}\n Release date: {release_date}\n Genre id: {genre_ids}\n' \
                 f' Original languare {original_language}\n Overwiew: {overview}\n Voteaverage: {vote_average}\n' \
                 f' Vote count: {vote_count}\n Popularity: {popularity}\n Genre id: {genre_ids}\n Movie_id: {id}\n' \
                 f' Poster path: https://image.tmdb.org/t/p/w500{poster_path}\n' \
                 f'------------------------------------------------------------------------------------------'
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)

    await callback.message.edit_text(text=text_value)
    await callback.message.edit_reply_markup(
        reply_markup=popular_movie_buttons(first, len(popular_list), original_name, id))


@dp.callback_query_handler(Text(startswith='title'))
async def choose_option(callback: types.CallbackQuery):
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)
    await FormTitle.title.set()
    await callback.message.answer('Enter Title Of Film:')


@dp.message_handler(state=FormTitle.title)
async def find_by_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Title is: ', md.bold(data['title'])),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=title_keyboard()
        )


@dp.callback_query_handler(Text(startswith='find'), state=FormTitle.title)
async def title(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            first = int(callback['data'].replace('find_', ''))
            name = data['title']
            movie_list = find_by_name(name)
            print(movie_list)

            id = movie_list[first]['id']
            genre_ids = movie_list[first]['genre_ids']
            original_name = movie_list[first]['original_title']
            original_language = movie_list[first]['original_language']
            overview = movie_list[first]['overview']
            vote_average = movie_list[first]['vote_average']
            vote_count = movie_list[first]['vote_count']
            release_date = movie_list[first]['release_date']
            popularity = movie_list[first]['popularity']
            poster_path = movie_list[first]['poster_path']

            text_value = f' Movie: {original_name}\n Release date: {release_date}\n Genre id: {genre_ids}\n' \
                         f' Original languare {original_language}\n Overwiew: {overview}\n Voteaverage: {vote_average}\n' \
                         f' Vote count: {vote_count}\n Popularity: {popularity}\n Genre id: {genre_ids}\n Movie_id: {id}\n' \
                         f' Poster path: https://image.tmdb.org/t/p/w500{poster_path}\n' \
                         f'-------------------------------------------------------------------------------------------------'
            # For "typing" message in top console
            await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
            await asyncio.sleep(1)

            await callback.message.edit_text(text=text_value)
            await callback.message.edit_reply_markup(
                reply_markup=title_movie_buttons(first, len(movie_list), original_name, id))
    except IndexError as ex:
        await state.finish()
        await callback.message.reply('Sorry. No Results', reply_markup=menu_())


@dp.callback_query_handler(Text(startswith='finish'), state=FormTitle)
async def passing(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(text="Thnx For Using This Bot 🤖!")
    await state.finish()


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)

    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)

    # Cancel state and inFormCriteria user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(Text(startswith='criteria'))
async def choose_option(callback: types.CallbackQuery):
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)
    await FormCriteria.genre.set()
    await callback.message.answer('Choose Genre:',
                                  reply_markup=genres)


@dp.message_handler(state=FormCriteria.genre)
async def process_genre(message: types.Message, state: FSMContext):
    """
    Process genre edit
    """
    async with state.proxy() as data:
        data['genre'] = message.text

    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)

    await FormCriteria.next()
    await message.answer('Enter Vote Average: ',
                         reply_markup=vote_average)


@dp.message_handler(lambda message: not message.text.isdigit(), state=FormCriteria.voteaverage)
async def process_vote_average_invalid(message: types.Message):
    """
    if vote average is invalid
    """
    return await message.answer('Vote average may be a number. \n Rate it! (digits only)')


@dp.message_handler(lambda message: message.text.isdigit(), state=FormCriteria.voteaverage)
async def process_voteaverage(message: types.Message, state: FSMContext):
    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)

    # Update state and data
    await FormCriteria.next()
    await state.update_data(voteaverage=int(message.text))
    await message.answer("What is the Year?", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: not message.text.isdigit(), state=FormCriteria.year)
async def process_year_invalid(message: types.Message):
    """
    if year is invalid
    """
    return await message.reply('Year may be a number. \n Example: 1999 (digits only)')


@dp.message_handler(state=FormCriteria.year)
async def process_year(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['year'] = message.text

        # For "typing" message in top console
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(1)

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Genre is: ', md.bold(data['genre'])),
                md.text('Minimum Vote Average:', md.code(data['voteaverage'])),
                md.text('Minimum Year:', data['year']),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=total_keyboard()
        )


@dp.callback_query_handler(Text(startswith='total'), state=FormCriteria.year)
async def total(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            first = int(callback['data'].replace('total_', ''))

            genre = data['genre']
            voteaverege = data['voteaverage']
            year = data['year']
            api_version = 3
            api_base_url = f'https://api.themoviedb.org/{api_version}'
            endpoint_path = f'/discover/movie'
            endpoint = f'{api_base_url}{endpoint_path}?api_key={api_key}' \
                       f'&sort_by=popularity.desc&include_adult=false&include_video=false&vote_count.gte=200' \
                       f'&with_genres={genre}&vote_average.gte={voteaverege}&primary_release_year={year}'

            r = requests.get(endpoint)
            data = r.json()
            print(len(data))

            id = data['results'][first]['id']
            # genre_ids = data['results'][first]['genre_ids']
            original_name = data['results'][first]['original_title']
            original_language = data['results'][first]['original_language']
            overview = data['results'][first]['overview']
            vote_average = data['results'][first]['vote_average']
            vote_count = data['results'][first]['vote_count']
            release_date = data['results'][first]['release_date']
            popularity = data['results'][first]['popularity']
            poster_path = data['results'][first]['poster_path']

            text_value = f' Movie: {original_name}\n Release date: {release_date}\n ' \
                         f' Original languare {original_language}\n Overwiew: {overview}\n Voteaverage: {vote_average}\n' \
                         f' Vote count: {vote_count}\n Popularity: {popularity}\n Movie_id: {id}\n' \
                         f' Poster path: https://image.tmdb.org/t/p/w500/{poster_path}\n' \
                         f'------------------------------------------------------------------------------------------'

            # For "typing" message in top console
            await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
            await asyncio.sleep(0.25)

            await callback.message.edit_text(text=text_value)
            await callback.message.edit_reply_markup(reply_markup=result_keyboard(first, len(data), original_name, id))
    except IndexError as ex:
        await state.finish()
        await callback.message.reply('Sorry. No Results', reply_markup=menu_())



@dp.callback_query_handler(Text(startswith='finish'), state=FormCriteria)
async def passing(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(text="Thnx For Using This Bot 🤖!")
    await state.finish()
