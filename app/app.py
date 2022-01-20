from loader import bot


async def on_shutdown(dp):
    await bot.close()


if __name__ == '__main__':
    print('It is Work!')
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)
