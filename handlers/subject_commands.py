import peewee
from aiogram.types import Message, ReplyKeyboardRemove, ContentTypes, KeyboardButton
from aiogram.dispatcher import FSMContext

from database import Subject, Deadline
from state_machine import StateMachine
from keyboards import create_markup


async def process_create_subject(message: Message, state: FSMContext):
    await state.update_data(type="CreateNewSubject")
    await StateMachine.waiting_for_create_subject.set()
    await message.answer("Enter new subject name")


async def process_delete_subject(message: Message, state: FSMContext):
    query = Subject.select().where(Subject.user == message.from_id).order_by(Subject.subject.asc())
    keyboard: peewee.ModelDictCursorWrapper[Subject] = query.execute()
    if len(keyboard) == 0:
        await message.answer("Subject list is empty")
        return

    keyboard_markup = create_markup([i.subject for i in keyboard], 3)
    await state.update_data(type="DeleteSubject")
    await StateMachine.waiting_for_delete_subject.set()
    await message.answer("Select subject for delete", reply_markup=keyboard_markup)


async def process_end_creating_subject(message: Message, state: FSMContext):
    await state.finish()

    query: peewee.ModelDictCursorWrapper = Subject.select().where(Subject.user == message.from_id and
                                                                  Subject.subject == message.text).execute()
    if len(query) > 0:
        await message.answer("This subject already exists")
        return

    Subject.create(user=message.from_id, subject=message.text)
    await message.answer("Done")


async def process_end_deleting_subject(message: Message, state: FSMContext):
    await state.finish()
    query: peewee.ModelDictCursorWrapper = Subject.select().where(Subject.user == message.from_id and
                                                                  Subject.subject == message.text).execute()
    if len(query) == 0:
        await message.answer("This subject does not exists", reply_markup=ReplyKeyboardRemove())
        return

    Deadline.delete().where(Deadline.user == message.from_id and Deadline.subject == message.text).execute()
    Subject.delete().where(Subject.user == message.from_id and Subject.subject == message.text).execute()
    await message.answer("Done", reply_markup=ReplyKeyboardRemove())
