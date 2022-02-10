from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext

from config import ADMIN_ID
from database.db import User
from keyboards.inline.language import get_markup
from loader import _, bot, dp
from states.mailing import FormMailing


@dp.message_handler(user_id=ADMIN_ID, commands=["mail"])
async def mailing(message: types.Message):
    await message.answer(_("Send Your Mailing Text"))
    await FormMailing.text.set()


@dp.message_handler(user_id=ADMIN_ID, state=FormMailing.text)
async def enter_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.answer(
        _("What Is The Language Of Mailing? \n\n" "Text: \n" "{text}").format(
            text=text
        ),
        reply_markup=get_markup(),
    )
    await FormMailing.language.set()


@dp.callback_query_handler(user_id=ADMIN_ID, state=FormMailing.language)
async def enter_lang(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    await state.reset_state()
    await callback.message.edit_reply_markup()
    users = await User.query.where(User.language == callback.data).gino.all()
    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id, text=text)
            await sleep(0.3)
        except Exception:
            pass
    await callback.message.answer(_("Mailing Success"))
