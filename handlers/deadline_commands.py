import peewee
from aiogram.types import Message, ReplyKeyboardRemove, ContentTypes, KeyboardButton
from aiogram.dispatcher import FSMContext
from datetime import datetime

from database import Subject, Deadline
from state_machine import StateMachine
from keyboards import create_markup

from datetime import date
import re

from functions import get_date


async def process_add_deadline(message: Message, state: FSMContext):
    query = Subject.select().where(Subject.user == message.from_id).order_by(Subject.subject.asc())
    keyboard: peewee.ModelDictCursorWrapper[Deadline] = query.execute()
    if len(keyboard) == 0:
        await message.answer("Subject list is empty, please add subjects to continue")
        return

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
    await message.answer("Please, write deadline in format DD.MM.YYYY or DD.MM (if year is current) and time in "
                         "format HH:MM or start-end HH:MM-HH:MM if needed")


async def process_add_deadline_get_date(message: Message, state: FSMContext):
    try:
        info = message.text.split()
        if info[0].count('.') == 1:
            info[0] += f".{date.today().year}"
        deadline_date = datetime.strptime(info[0], "%d.%m.%Y").date()
        deadline_time = None if len(info) == 1 else info[1]

        if deadline_time:
            if len(deadline_time) not in [5, 11]:
                raise ValueError
            if len(deadline_time) == 11 and re.match(r"\d{2}:\d{2}-\d{2}:\d{2}", deadline_time) is None:
                raise ValueError
            if len(deadline_time) == 5 and re.match(r"\d{2}:\d{2}", deadline_time) is None:
                raise ValueError

    except ValueError:
        await message.answer("Please, enter valid date and time")
        return

    data = await state.get_data()
    await state.finish()

    Deadline.create(user=message.from_id,
                    subject=data['subject'],
                    task=data['task'],
                    deadline=deadline_date,
                    time=deadline_time
                    )
    await message.answer("New deadline created")


async def process_list_deadlines(message: Message):
    query = Deadline.select().where(Deadline.user == message.from_id).order_by(Deadline.deadline.asc()).execute()
    query: peewee.ModelDictCursorWrapper[Deadline]
    texts = [f"{i.subject}: {i.task} ({get_date(i.deadline, i.time)})" for i in query]

    if not texts:
        await message.answer("You haven't got any deadlines :)")
        return

    await message.answer("Your tasks:\n" + "\n".join(texts))


async def process_delete_deadline(message: Message):
    query = Subject.select().where(Subject.user == message.from_id).order_by(Subject.subject.asc())
    keyboard: peewee.ModelDictCursorWrapper[Deadline] = query.execute()
    if len(keyboard) == 0:
        await message.answer("Subject list is empty, please add subjects to continue")
        return

    await StateMachine.waiting_for_deadline_delete_subject.set()
    keyboard_markup = create_markup([i.subject for i in keyboard], 3)
    await message.answer("Choose subject from given list", reply_markup=keyboard_markup)


async def process_delete_deadline_get_subject(message: Message, state: FSMContext):
    query = Subject.select().where(Subject.user == message.from_id).execute()
    query: peewee.ModelDictCursorWrapper[Subject]
    if not query:
        await message.answer("Please, select subject from keyboard")
        return

    tasks = Deadline.select().where(Deadline.user == message.from_id, Deadline.subject == message.text).execute()
    if not tasks:
        await message.answer("No deadlines on this subject")
        return

    await state.update_data(subject=message.text)
    await StateMachine.waiting_for_deadline_delete_task.set()
    keyboard_markup = create_markup([i.task for i in tasks], 3)
    await message.answer("Please, select task from keyboard", reply_markup=keyboard_markup)


async def process_delete_deadline_get_task(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text[-1] == "…":
        message.text = message.text[:-1]
    Deadline.delete().where(Deadline.user == message.from_id,
                            Deadline.subject == data['subject'],
                            Deadline.task.startswith(message.text)
                            ).execute()

    await state.finish()
    await message.answer("Done", reply_markup=ReplyKeyboardRemove())
