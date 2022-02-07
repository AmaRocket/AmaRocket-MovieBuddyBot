from database import db
from loader import bot


async def on_startup(_):
    print("GO GO GO")
    await db.create_db()


async def on_shutdown(p):
    await bot.close()


if __name__ == "__main__":
    print("It is Work!")
    from aiogram import executor

    from handlers import dp

    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
