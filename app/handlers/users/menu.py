import logging
import re

import aiogram.utils.markdown as md

from aiogram import types
from aiogram.dispatcher import FSMContext

from data_base.db import User, Title, Criteria, DBCommands, MyMovies

from states.criteria import FormCriteria

from TEST_TMDB_PIPY import TheMovie

# from config import DB_URI
from keyboards.default import vote_average

from keyboards.inline.choise_buttons import popular_movie_buttons, menu_, title_movie_buttons, total_keyboard, \
    result_keyboard, title_keyboard, genres_keyboard, start, similar_movie_keyboard
from loader import dp, bot
from aiogram.types import Message, ParseMode

from aiogram.dispatcher.filters import Command, Text

import asyncio
from aiogram.types import ChatActions

# ================ DATA BASE SETTINGS =================================================================================

db = DBCommands()


# =====================================================================================================================


# ================ START FUNCTIONS + ADD USER TO DB ====================================================================
@dp.message_handler(Command('start'))
async def start_menu(message: Message):
    user_id = message.from_user.id
    username = message.from_user.first_name

    user = await db.add_new_user()  # add user in db

    id = user.id  # For Change lang

    count_users = await db.count_users()  # Count users for admin (in future mb)
    print(count_users)

    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)

    await message.reply(f'Hello {username}. \nSelect Your Option From Menu 👇', reply_markup=start())


@dp.message_handler(lambda message: True, content_types='text')
async def user_message(message):
    user_id = message.from_user.id
    # update_messages_count(user_id)


# =====================================================================================================================


# ================ MY_MOVIES ==========================================================================================

@dp.callback_query_handler(Text(startswith='movie_list'))
async def movie_list(callback: types.CallbackQuery):
    """

    :param callback:
    :return:
    """
    await callback.message.reply('It Wll Be Work Soon ✌️')
    await callback.answer()


@dp.callback_query_handler(Text(startswith='add_to_movie_list'))
async def add_to_movie_list(callback: types.CallbackQuery):
    """
    Function for add movie to db list

    :param callback:
    :return:
    """
    item = MyMovies()
    data = callback.get_current().message.text

    movie_id = (re.findall(r'ID: (\d+)', data))
    m_id = int(movie_id[-1])

    user_id = int(types.User.get_current())

    item.users_id = user_id
    item.movie_id = m_id
    item.data = data

    await item.create()

    await callback.answer(text='Added To Your MovieList')


# =====================================================================================================================


# ================ MOVIES =============================================================================================

@dp.callback_query_handler(Text(startswith='movies'))
async def movies(callback: types.CallbackQuery):
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await callback.message.reply('Choose The Option 👇', reply_markup=menu_())
    await callback.answer()


# List Of Popular Movies
@dp.callback_query_handler(Text(startswith='popular'))
async def poppular_by(callback: types.CallbackQuery):
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


# Find Movie By Title
@dp.callback_query_handler(Text(startswith='title'))
async def choose_option(callback: types.CallbackQuery):
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await FormCriteria.title.set()
    await callback.message.answer('Enter Title Of Film:')


# Find Movie By Title
@dp.message_handler(state=FormCriteria.title)
async def find_by_title(message: types.Message, state: FSMContext):
    # user_id = message.from_user.id

    async with state.proxy() as data:
        data['title'] = message.text

        item = Title()
        # user = User()
        user_id = types.User.get_current()
        item.title = data['title']
        item.users_id = user_id
        await state.update_data(item=item)

        data = await state.get_data()
        item: Title = data.get('item')

        await item.create()
        await message.reply(text=item.title, reply_markup=title_keyboard())

        await state.reset_state()

        # await bot.send_message(
        #     message.chat.id,
        #     md.text(
        #         md.text('Title is: ', md.bold(data['title'])),
        #         sep='\n',
        #     ),
        #     parse_mode=ParseMode.MARKDOWN_V2,
        #     reply_markup=title_keyboard()
        # )
        #
        #
        #


# =====================================================================================================================

# Find Movie By Title
@dp.callback_query_handler(Text(startswith='find'))  # , state=FormCriteria.title)
async def title(callback: types.CallbackQuery):  # , state: FSMContext):
    try:
        # async with state.proxy() as data:
        first = int(callback['data'].replace('find_', ''))

        title = await db.show_title()
        print(title)
        for i in title:
            print(i)

        # name = data['title']
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
    except IndexError as ex:
        # await state.finish()
        await callback.message.reply('Sorry. No Results', reply_markup=menu_())


@dp.callback_query_handler(Text(startswith='finish'), state=FormCriteria)
async def passing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.reply('Select Your Option From Menu👇🏻', reply_markup=menu_())
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
    await asyncio.sleep(0.5)

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


# =====================================================================================================================

@dp.callback_query_handler(Text(startswith='criteria'))
async def choose_option(callback: types.CallbackQuery):
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await FormCriteria.genre.set()
    await callback.message.reply('Choose Genre:',
                                 reply_markup=genres_keyboard())


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
    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    # Update state and data
    await FormCriteria.next()
    await state.update_data(voteaverage=int(message.text))

    data = await state.get_data()
    item: Criteria = data.get('item')
    vote_average = int(message.text)
    item.vote_average = vote_average
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
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['year'] = message.text

        data = await state.get_data()
        item: Criteria = data.get('item')
        year = int(message.text)
        item.year = year
        item.users_id = user_id

        await item.create()

        await state.reset_state()

        # For "typing" message in top console
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.3)

        await message.reply(text=(item.genre, item.vote_average, item.year), reply_markup=total_keyboard())

        # await bot.send_message(
        #     message.chat.id,
        #     md.text(
        #         md.text('Genre is: ', md.bold(data['genre'])),
        #         md.text('Minimum Vote Average:', md.code(data['voteaverage'])),
        #         md.text('Minimum Year:', data['year']),
        #         sep='\n',
        #     ),
        #     parse_mode=ParseMode.MARKDOWN_V2,
        #     reply_markup=total_keyboard()
        # )
        # print(item.genre, item.vote_average, item.year)


@dp.callback_query_handler(Text(startswith='total'))
async def total(callback: types.CallbackQuery):
    try:
        first = int(callback['data'].replace('total_', ''))

        criteria = await db.show_criteria()
        print(criteria)
        for i in criteria:
            # print(i)

            genre = i.genre
            print(genre)
            voteaverage = i.vote_average
            print(voteaverage)
            year = i.year
            print(year)
            print('==========')

        movie_list = TheMovie().discover.discover_movies({
            'sort_by': 'popularity.desc',
            'vote_count.gte': '',
            'with_genres': f'{genre}',
            'vote_average.gte': f'{voteaverage}',
            'primary_release_year': f'{year}'
        })
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
        await asyncio.sleep(0.25)

        await callback.message.edit_text(text=text_value)
        await callback.message.edit_reply_markup(
            reply_markup=result_keyboard(first, len(movie_list), original_name, id))
    except IndexError as ex:
        # await state.finish()
        await callback.message.reply('Sorry. No Results', reply_markup=menu_())


# @dp.callback_query_handler(Text(startswith='total'), state=FormCriteria.year)
# async def total(callback: types.CallbackQuery, state: FSMContext):
#     try:
#         async with state.proxy() as data:
#             first = int(callback['data'].replace('total_', ''))
#             genre = data['genre']
#             voteaverage = data['voteaverage']
#             year = data['year']
#             # item = Criteria()
#             # genre = item.genre
#             # voteaverage = item.vote_average
#             # year = item.year
#             movie_list = TheMovie().discover.discover_movies({
#                 'sort_by': 'popularity.desc',
#                 'with_genres': f'{genre}',
#                 'vote_average.gte': f'{voteaverage}',
#                 'primary_release_year': f'{year}'
#             })
#             id = movie_list[first]['id']
#             genre_ids = movie_list[first]['genre_ids']
#             original_name = movie_list[first]['title']
#             original_language = movie_list[first]['original_language']
#             overview = movie_list[first]['overview']
#             vote_average = movie_list[first]['vote_average']
#             vote_count = movie_list[first]['vote_count']
#             release_date = movie_list[first]['release_date']
#             popularity = movie_list[first]['popularity']
#             poster_path = movie_list[first]['poster_path']
#
#             text_value = f' ID: {id}\n Movie: {original_name}\n Release date: {release_date}\n Genre id: {genre_ids}\n' \
#                          f' Original languare {original_language}\n Overwiew: {overview}\n Voteaverage: {vote_average}\n' \
#                          f' Vote count: {vote_count}\n Popularity: {popularity}\n Genre id: {genre_ids}\n ' \
#                          f' Poster path: https://image.tmdb.org/t/p/original{poster_path}\n' \
#                          f'------------------------------------------------------------------------------------------'
#
#             # For "typing" message in top console
#             await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
#             await asyncio.sleep(0.25)
#
#             await callback.message.edit_text(text=text_value)
#             await callback.message.edit_reply_markup(
#                 reply_markup=result_keyboard(first, len(movie_list), original_name, id))
#     except IndexError as ex:
#         await state.finish()
#         await callback.message.reply('Sorry. No Results', reply_markup=menu_())


# Similar Movies
@dp.callback_query_handler(Text(startswith='similar'))  # , state=FormCriteria)
async def movie_like_this(callback: types.CallbackQuery):  # state: FSMContext):
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
        # await state.finish()
        await callback.message.reply('Sorry. No Results', reply_markup=menu_())

# Similar Movies
# @dp.callback_query_handler(Text(startswith='similar'))  # , state=FormCriteria)
# async def movie_like_this(callback: types.CallbackQuery):  # state: FSMContext):
#     try:
#
#         # await state.finish()
#         message = callback.message.text
#
#         movie_id = (re.findall(r'ID: (\d+)', message))
#         m_id = movie_id[-1]
#
#         movie_list = TheMovie().movie.recommendations(m_id)
#         first = int(callback['data'].replace('similar_', ''))
#         print(first)
#         print(type(first))
#
#         id = movie_list[first]['id']
#         genre_ids = movie_list[first]['genre_ids']
#         original_name = movie_list[first]['title']
#         original_language = movie_list[first]['original_language']
#         overview = movie_list[first]['overview']
#         vote_average = movie_list[first]['vote_average']
#         vote_count = movie_list[first]['vote_count']
#         release_date = movie_list[first]['release_date']
#         popularity = movie_list[first]['popularity']
#         poster_path = movie_list[first]['poster_path']
#
#         text_value = f' ID: {id}\n Movie: {original_name}\n Release date: {release_date}\n Genre id: {genre_ids}\n' \
#                      f' Original languare {original_language}\n Overwiew: {overview}\n Voteaverage: {vote_average}\n' \
#                      f' Vote count: {vote_count}\n Popularity: {popularity}\n Genre id: {genre_ids}\n ' \
#                      f' Poster path: https://image.tmdb.org/t/p/original{poster_path}\n' \
#                      f'---------------------------------------------------------------------------------------------'
#
#         # For "typing" message in top console
#         await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
#         await asyncio.sleep(1)
#
#         await callback.message.edit_text(text=text_value)
#         await callback.message.edit_reply_markup(
#             reply_markup=similar_movie_keyboard(first, len(movie_list), original_name, id))
#
#     except IndexError as ex:
#         # await state.finish()
#         await callback.message.reply('Sorry. No Results', reply_markup=menu_())
