from aiogram import Bot, Dispatcher, executor, types
from handler import *



async def on_start(_):
    print('Бот запущен')



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)

