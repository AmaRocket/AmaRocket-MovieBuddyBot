import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatActions

from database.db import DBCommands
from keyboards.inline.choise_buttons import popular_movie_buttons
from loader import _, bot, dp
from message_output.message_output import MessageText
from tmdb_v3_api import get_api_for_context

# ================ DATA BASE SETTINGS =================================================================================


db = DBCommands()


# =====================================================================================================================

# ================ POPULAR ============================================================================================


@dp.callback_query_handler(Text(startswith="popular"))
async def poppular_by(callback: types.CallbackQuery):
    """

    :param callback:
    :return: list with popular movies from tmdbv3api
    """

    tmdb_with_language = await get_api_for_context(callback.message.chat.id)

    movie_list = tmdb_with_language.movie.popular()

    first = int(callback["data"].replace("popular_", ""))

    # Message List
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
        reply_markup=popular_movie_buttons(
            first, len(movie_list), message.original_title, message.movie_id
        )
    )


# =====================================================================================================================
