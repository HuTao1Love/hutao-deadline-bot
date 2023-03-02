from aiogram.dispatcher.filters.state import State, StatesGroup


class StateMachine(StatesGroup):
    waiting_for_subject = State()
    waiting_for_task = State()
    waiting_for_old_record = State()
    waiting_for_new_date = State()

    waiting_for_create_subject = State()
    waiting_for_delete_subject = State()
