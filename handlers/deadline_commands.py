import peewee
from aiogram.types import Message, ReplyKeyboardRemove, ContentTypes, KeyboardButton
from aiogram.dispatcher import FSMContext
from datetime import datetime

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
    query = Subject.select().where(Subject.user == message.from_id, Subject.subject == message.text).execute()
    query: peewee.ModelDictCursorWrapper[Subject]
    if not query:
        await message.answer("Please, select subject from keyboard")
        return

    await state.update_data(subject=message.text)
    await StateMachine.waiting_for_task.set()
    await message.answer("Please, write task", reply_markup=ReplyKeyboardRemove())


async def process_add_deadline_get_task(message: Message, state: FSMContext):
    await state.update_data(task=message.text)
    await StateMachine.waiting_for_date.set()
    await message.answer("Please, write deadline in format DD.MM.YYYY")


async def process_add_deadline_get_date(message: Message, state: FSMContext):
    try:
        deadline_date = datetime.strptime(message.text, "%d.%m.%Y")
        deadline_date = date(deadline_date.year, deadline_date.month, deadline_date.day)
    except ValueError:
        await message.answer("Please, enter valid date")
        return

    data = await state.get_data()
    await state.finish()

    Deadline.create(user=message.from_id,
                    subject=data['subject'],
                    task=data['task'],
                    deadline=deadline_date
                    )
    await message.answer("New deadline created")


async def process_list_deadlines(message: Message):
    query = Deadline.select().where(Deadline.user == message.from_id).order_by(Deadline.deadline.asc()).execute()
    query: peewee.ModelDictCursorWrapper[Deadline]
    texts = [f"{i.subject}: {i.task} ({i.deadline.strftime('%d.%m.%Y')})" for i in query]

    if not texts:
        await message.answer("You haven't got any deadlines :)")
        return

    await message.answer("Your tasks:\n" + "\n".join(texts))
