import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatActions

from keyboards.inline.choise_buttons import popular_movie_buttons
from loader import bot, dp
from message_output.message_output import MessageText
from tmdb_v3_api import TheMovie

# ================ POPULAR ============================================================================================


@dp.callback_query_handler(Text(startswith="popular"))
async def poppular_by(callback: types.CallbackQuery):
    """

    :param callback:
    :return: list with popular movies from tmdbv3api
    """
    movie_list = TheMovie().movie.popular()

    first = int(callback["data"].replace("popular_", ""))

    # Message List
    message = MessageText(movie_list[first])

    poster = "https://image.tmdb.org/t/p/original" + message.movie_image

    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await callback.message.edit_text(text=f"{message.message} {poster}")
    # await callback.message.edit_media(media=poster)
    await callback.message.edit_reply_markup(
        reply_markup=popular_movie_buttons(
            first, len(movie_list), message.original_title, message.movie_id
        )
    )


# =====================================================================================================================
