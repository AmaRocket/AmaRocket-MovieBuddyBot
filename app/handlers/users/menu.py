import asyncio

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ChatActions, Message

from database.db import DBCommands
from keyboards.inline.choise_buttons import menu_, start, starting
from keyboards.inline.language import get_markup
from loader import _, bot, dp

# ================ DATA BASE SETTINGS =================================================================================


db = DBCommands()


# =====================================================================================================================

# ================ START FUNCTIONS + ADD USER TO DB ====================================================================
@dp.message_handler(CommandStart())
async def start_menu(message: Message):
    """

    :param message:
    :return: start keyboard and add user info in Users Table
    """

    username = message.from_user.first_name

    count_users = await db.count_users()  # Count users for admin (in future mb)
    print(count_users)

    # For "typing" message in top console
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.25)

    await db.add_new_user()  # add user in db

    with open("../media/futurama-1644426466304-7977.jpg", "rb") as img:
        await bot.send_photo(
            message.chat.id,
            img,
            _("<b>Choose The Language {username}</b>").format(username=username),
            reply_markup=get_markup(),
        )


@dp.callback_query_handler(text_contains="lang")
async def change_language(callback: types.CallbackQuery):
    username = callback.message.from_user.first_name
    await callback.message.edit_reply_markup()
    lang = callback.data[-2:]

    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.25)

    await db.set_language(lang)

    await dp.middleware.trigger("set_language", {})

    await callback.answer(_("Your Language Was Changed", locale=lang))
    with open("../media/photo_2022-02-03_01-21-05.jpg", "rb") as img:
        await bot.send_photo(
            callback.message.chat.id,
            img,
            _(
                "<b>Hey! I Am {username}\nBuddy I Can Help U With:\n\n🔍 🔸 Find A Movie \n\n"
                "📝 🔸 Add It Your Movie List \n\n"
                "📺 🔸 Watch Trailer On YouTube  \n\nℹ 🔸 Watch Info On TMDB ️\n\n"
                "⚡ 🔸 And Yes! I Am Powered By TMDB󠁴</b>"
            ).format(username=username),
            reply_markup=starting(),
        )


@dp.callback_query_handler(Text(equals="go"))
async def starter(callback: types.CallbackQuery):

    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.25)

    await callback.message.reply(
        _("Find Movie Or Check Your Movie List 👇"), reply_markup=start()
    )
    await callback.answer()


# =====================================================================================================================

# ================ MOVIES =============================================================================================


@dp.callback_query_handler(Text(startswith="movies"))
async def movies(callback: types.CallbackQuery):
    """

    :param callback:
    :return: menu keyboard
    """
    # For "typing" message in top console
    await bot.send_chat_action(callback.message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(0.25)

    await callback.message.reply(_("Choose The Option 👇"), reply_markup=menu_())
    await callback.answer()
