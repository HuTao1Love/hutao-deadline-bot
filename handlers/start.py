from datetime import datetime, timedelta

from aiogram import types, Bot
from database import Subject, Deadline

from config import CREATOR_ID


async def process_start(message: types.Message):
    await message.answer(f'Hi, {message.from_user.full_name}!\nI will help to control your deadlines!')


async def process_shutdown(message: types.Message):
    if message.from_id != CREATOR_ID:
        await message.answer("You cannot do that")
        return

    await message.answer("Shutdown")
    exit(0)


async def process_check_deadlines(message: types.Message = None, api: Bot = None):
    query = Deadline.select().where(Deadline.deadline <= datetime.today().date()).execute()
    for i in query:
        if message:
            api = message.bot
        await api.send_message(i.user, f"Deadline {i.subject}: {i.description}")
        if i.deadline < datetime.today().date() - timedelta(days=2):
            i.delete_instance()

    query = Deadline.select().where(Deadline.deadline == datetime.today().date() + timedelta(days=1)).execute()
    for i in query:
        if message:
            api = message.bot
        await api.send_message(i.user, f"Tomorrow deadline {i.subject}: {i.description}")
