from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import handlers

from config import API_TOKEN

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)

handlers.setup(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)