from aiogram import types

from config import CREATOR_ID


async def process_start(message: types.Message):
    await message.answer(f'Hi, {message.from_user.full_name}!\nI will help to control your deadlines!')


async def process_shutdown(message: types.Message):
    if message.from_id != CREATOR_ID:
        await message.answer("You cannot do that")
        return

    await message.answer("Shutdown")
    exit(0)