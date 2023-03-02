from aiogram import types


async def process_start(message: types.Message):
    await message.answer(f'Hi, {message.from_user.full_name}!\nI will help to control your deadlines!')
