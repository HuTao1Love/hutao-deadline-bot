import peewee
from aiogram.types import Message, ReplyKeyboardRemove, ContentTypes, KeyboardButton
from aiogram.dispatcher import FSMContext

from database import Subject, Deadline
from state_machine import StateMachine
from keyboards import create_markup

from datetime import date


async def process_add_deadline(message: Message, state: FSMContext):
    # Deadline.create(user=message.from_id, subject="Алгосики", task="Лаба", deadline=date(2023, 3, 3))
    query = Subject.select().where(Subject.user == message.from_id).order_by(Subject.subject.asc())
    keyboard: peewee.ModelDictCursorWrapper[Deadline] = query.execute()
    if len(keyboard) == 0:
        await message.answer("Subject list is empty, please add subjects to continue")
        return

    await state.update_data(type="CreateNewDeadline")
    await StateMachine.waiting_for_subject.set()

    keyboard_markup = create_markup([i.subject for i in keyboard], 3)
    await message.answer("Choose subject from given list", reply_markup=keyboard_markup)


async def process_add_deadline_get_subject(message: Message, state: FSMContext):



async def process_list_deadlines(message: Message, state: FSMContext):
    query = Deadline.select().where(Deadline.user == message.from_id).order_by(Deadline.deadline.asc()).execute()
    query: peewee.ModelDictCursorWrapper[Deadline]
    texts = [f"{i.subject}: {i.task} ({i.deadline})" for i in query]

    if not texts:
        await message.answer("You haven't got any deadlines :)")
        return

    await message.answer("Your tasks:\n" + "\n".join(texts))
