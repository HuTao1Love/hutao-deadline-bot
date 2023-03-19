from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import handlers
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import API_TOKEN

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)


async def on_startup(dp: Dispatcher):
    await handlers.setup(dp)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(handlers.process_check_deadlines, 'cron', hour=0, minute=0, kwargs={'api': bot})
    scheduler.start()


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
