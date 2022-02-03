import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from data_base.db import DBCommands

from states.criteria import FormCriteria

from keyboards.inline.choise_buttons import menu_, start, starting
from loader import dp, bot
from aiogram.types import Message

from aiogram.dispatcher.filters import Command, Text

import asyncio
from aiogram.types import ChatActions

# ================ DATA BASE SETTINGS =================================================================================

db = DBCommands()


# =====================================================================================================================

# ================ START FUNCTIONS + ADD USER TO DB ====================================================================
@dp.message_handler(Command('start'))
async def start_menu(message: Message):
    """

    :param message:
    :return: start keyboard and add user info in Users Table
    """
    user_id = message.from_user.id
    username = message.from_user.first_name
    user = await db.add_new_user()  # add user in db

    # id = user.id  # For Change lang

    count_users = await db.count_users()  # Count users for admin (in future mb)
    print(count_users)

    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)

    with open('photo_2022-02-03_01-21-05.jpg', 'rb') as img:
        await bot.send_photo(message.chat.id, img,
                             caption=f'<b>Hello {username}!\nBuddy I Can Help U With:\n\n🔍 🔸 Find A Movie \n\n'
                                     f'📝 🔸 Add It Your Movie List \n\n'
                                     f'📺 🔸 Watch Trailer On YouTube  \n\nℹ 🔸 Watch Info On TMDB ️\n\n'
                                     f'⚡ 🔸 And Yes! I Am Powered By TMDB󠁴</b>', reply_markup=starting())


@dp.callback_query_handler(Text(equals='go', ignore_case=True))
async def starter(callback: types.CallbackQuery):
    await callback.message.reply('Find Movie Or Check Your Movie List 👇', reply_markup=start())
    await callback.answer()


# =====================================================================================================================

# ================ MOVIES =============================================================================================

@dp.callback_query_handler(Text(startswith='movies'))
async def movies(callback: types.CallbackQuery):
    """

    :param callback:
    :return: menu keyboard
    """
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.5)

    await callback.message.reply('Choose The Option 👇', reply_markup=menu_())
    await callback.answer()


# ================ CANCEL CHOOSE ======================================================================================


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
