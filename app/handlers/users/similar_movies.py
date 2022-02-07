import asyncio
import re

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatActions

from keyboards.inline.choise_buttons import menu_, similar_movie_keyboard
from loader import bot, dp
from message_output.message_output import MessageText
from tmdb_v3_api import TheMovie

# ================ SIMILAR ============================================================================================


@dp.callback_query_handler(Text(startswith="similar"))
async def movie_like_this(callback: types.CallbackQuery):
    """

    :param callback:
    :return: similar movies by move_id
    """
    try:
        message = callback.message.text

        movie_id = (re.findall(r"ID: (\d+)", message))[-1]

        movie_list = TheMovie().movie.recommendations(movie_id)
        first = int(callback["data"].replace("similar_", ""))

        message = MessageText(movie_list[first])
        poster = "https://image.tmdb.org/t/p/original" + message.movie_image

        # For "typing" message in top console
        await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(1)

        await callback.message.edit_text(text=f"{message.message} {poster}")
        await callback.message.edit_reply_markup(
            reply_markup=similar_movie_keyboard(
                first, len(movie_list), message.original_title, message.movie_id
            )
        )
    except IndexError:
        await callback.message.reply("Sorry. No Results", reply_markup=menu_())


# =====================================================================================================================
