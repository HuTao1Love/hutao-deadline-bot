from aiogram.dispatcher.filters.state import State, StatesGroup


class StateMachine(StatesGroup):
    waiting_for_deadline_delete_subject = State()
    waiting_for_deadline_delete_task = State()
    waiting_for_subject = State()
    waiting_for_task = State()
    waiting_for_date = State()

    waiting_for_create_subject = State()
    waiting_for_delete_subject = State()
