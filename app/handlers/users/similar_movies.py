import re

from aiogram import types
from aiogram.dispatcher.filters import Text

from TEST_TMDB_PIPY import TheMovie

from keyboards.inline.choise_buttons import similar_movie_keyboard, menu_
from loader import dp, bot

import asyncio
from aiogram.types import ChatActions


# ================ SIMILAR ============================================================================================
from message_output.message_output import MessageText


@dp.callback_query_handler(Text(startswith='similar'))
async def movie_like_this(callback: types.CallbackQuery):
    """

    :param callback:
    :return: similar movies by move_id
    """
    try:
        message = callback.message.text

        movie_id = ((re.findall(r'ID: (\d+)', message))[-1])

        movie_list = TheMovie().movie.recommendations(movie_id)
        first = int(callback['data'].replace('similar_', ''))

        text_value = MessageText().message(movie_list, first)

        original_name = text_value[2]

        # For "typing" message in top console
        await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(1)

        await callback.message.edit_text(text=text_value)
        await callback.message.edit_reply_markup(
            reply_markup=similar_movie_keyboard(first, len(movie_list), original_name, movie_id))
    except IndexError:
        await callback.message.reply('Sorry. No Results', reply_markup=menu_())

# =====================================================================================================================
