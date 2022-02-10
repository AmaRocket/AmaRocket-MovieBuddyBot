import asyncio
import datetime
import logging
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatActions

from database.db import Criteria, DBCommands
from keyboards.default import vote_average
from keyboards.inline.choise_buttons import (genres_keyboard, menu_,
                                             result_keyboard, total_keyboard)
from loader import _, bot, dp
from message_output.message_output import MessageText
from states.criteria import FormCriteria
from tmdb_v3_api import get_api_for_context

# ================ DATA BASE SETTINGS =================================================================================

db = DBCommands()


# =====================================================================================================================

# ================ CANCEL CHOOSE ======================================================================================


@dp.callback_query_handler(Text(startswith=["finish"]), state=FormCriteria)
async def passing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.reply(
        _("Select Your Option From Menu👇🏻"), reply_markup=menu_()
    )
    await callback.answer(text=_("Thnx For Using This Bot 🤖!"))
    await state.finish()


# You can use state '*' if you need to handle all states
@dp.message_handler(state="*", commands=["cancel"])
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)

    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.25)

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply(_("Cancelled."), reply_markup=types.ReplyKeyboardRemove())


# =====================================================================================================================


@dp.callback_query_handler(Text(startswith="criteria"))
async def choose_option(callback: types.CallbackQuery):
    """

    :param callback:
    :return: genres keyboard
    """
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.25)

    await FormCriteria.genre.set()
    await callback.message.reply(_("Choose Genre:"), reply_markup=genres_keyboard())
    await callback.answer()


@dp.callback_query_handler(state=FormCriteria.genre)
async def process_genre(callback: types.CallbackQuery, state: FSMContext):
    """
    Process genre edit
    """
    async with state.proxy() as data:
        data["genre"] = callback.data

    genre = int(callback.data)
    item = Criteria()
    item.genre = genre
    await state.update_data(item=item)

    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.25)

    await FormCriteria.next()
    await callback.message.answer(_("Enter Vote Average: "), reply_markup=vote_average)


@dp.message_handler(
    lambda message: not message.text.isdigit(), state=FormCriteria.voteaverage
)
async def process_vote_average_invalid(message: types.Message):
    """
    if vote average is invalid
    """
    return await message.answer(
        _("Vote average may be a number. \n Rate it! (digits only)")
    )


@dp.message_handler(
    lambda message: message.text.isdigit(), state=FormCriteria.voteaverage
)
async def process_voteaverage(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return: input year message
    """
    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.25)

    # Update state and data
    await FormCriteria.next()
    await state.update_data(voteaverage=int(message.text))

    data = await state.get_data()
    item: Criteria = data.get("item")
    voteaverage = int(message.text)
    item.vote_average = voteaverage
    await state.update_data(item=item)

    await message.answer(
        _("What is the Year?"), reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(lambda message: not message.text.isdigit(), state=FormCriteria.year)
async def process_year_invalid(message: types.Message):
    """
    if year is invalid
    """
    return await message.reply(
        _("Year may be a number. \n Example: 1999 (digits only)")
    )


@dp.message_handler(state=FormCriteria.year)
async def process_year(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return: confirmation request search by criteria
    """
    user_id = message.from_user.id
    async with state.proxy() as data:
        data["year"] = message.text

        data = await state.get_data()
        item: Criteria = data.get("item")
        year = int(message.text)
        item.year = year
        item.users_id = user_id
        item.time = datetime.datetime.now()

        await item.create()

        await state.reset_state()

        # For "typing" message in top console
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.25)

        item.year = item.year
        item.vote_average = item.vote_average
        item.genre = item.genre

        text = _(
            "<b> Genre ID: </b>{genre}\n"
            "<b> Vote Average </b>{vote_average}\n"
            "<b> Year </b>{year}\n"
        ).format(genre=item.genre, vote_average=item.vote_average, year=item.year)

        img = open("../media/futurama-fry-gif-wallpaper-futurama-1668529063.jpg", "rb")
        await bot.send_photo(message.chat.id, photo=img)
        await sleep(1)

        await message.answer(f"{text}", reply_markup=total_keyboard())


@dp.callback_query_handler(Text(startswith="total"))
async def total(callback: types.CallbackQuery):
    """

    :param callback:
    :return: list of movies by criteria
    """
    try:
        first = int(callback["data"].replace("total_", ""))

        criteria = await db.show_criteria()

        i = str()
        for index in criteria:
            i = index

        genre = i.genre
        voteaverage = i.vote_average
        year = i.year

        tmdb_with_language = await get_api_for_context(callback.message.chat.id)

        movie_list = tmdb_with_language.discover.discover_movies(
            {
                "sort_by": "popularity.desc",
                "vote_count.gte": "",
                "with_genres": f"{genre}",
                "vote_average.gte": f"{voteaverage}",
                "primary_release_year": f"{year}",
            }
        )

        message = MessageText(movie_list[first])

        if message.movie_image is None:
            poster = "https://image.tmdb.org/t/p/original"
        else:
            poster = "https://image.tmdb.org/t/p/original" + message.movie_image

        # For "typing" message in top console
        await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.25)

        await callback.message.edit_text(
            _("{message.message} {poster}").format(message=message, poster=poster)
        )
        await callback.message.edit_reply_markup(
            reply_markup=result_keyboard(
                first, len(movie_list), message.original_title, message.movie_id
            )
        )
    except IndexError:
        await callback.message.reply(_("Sorry. No Results"), reply_markup=menu_())


# =====================================================================================================================
