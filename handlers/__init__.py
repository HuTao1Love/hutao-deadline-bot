from aiogram import Dispatcher
from state_machine import StateMachine

from .command_classes import Command, StateCommand

from .start import (
    process_start,
    process_shutdown,
    process_check_deadlines
)
from .subject_commands import (
    process_create_subject,
    process_delete_subject,
    process_end_creating_subject,
    process_end_deleting_subject
)

from .deadline_commands import (
    process_add_deadline,
    process_add_deadline_get_subject,
    process_add_deadline_get_task,
    process_add_deadline_get_date,
    process_list_deadlines,
    process_delete_deadline,
    process_delete_deadline_get_subject,
    process_delete_deadline_get_task
)


commands = [
    Command(process_add_deadline, ['new_deadline', 'add_deadline', 'new', 'add'], "Create new deadline"),
    Command(process_list_deadlines, ['list_deadlines', 'list'], "Check your deadlines"),
    Command(process_delete_deadline, 'delete_deadline', "Delete deadline"),

    Command(process_start, 'start', "Start"),
    Command(process_shutdown, 'shutdown', ""),
    Command(process_create_subject, ['new_subject', 'create_subject'], "Create new subject"),
    Command(process_delete_subject, 'delete_subject', "Delete existing subject"),
    Command(process_check_deadlines, 'check_deadlines', "Check deadlines"),

    StateCommand(process_end_creating_subject, StateMachine.waiting_for_create_subject),
    StateCommand(process_end_deleting_subject, StateMachine.waiting_for_delete_subject),

    StateCommand(process_add_deadline_get_subject, StateMachine.waiting_for_subject),
    StateCommand(process_add_deadline_get_task, StateMachine.waiting_for_task),
    StateCommand(process_add_deadline_get_date, StateMachine.waiting_for_date),
    StateCommand(process_delete_deadline_get_subject, StateMachine.waiting_for_deadline_delete_subject),
    StateCommand(process_delete_deadline_get_task, StateMachine.waiting_for_deadline_delete_task)
]


async def setup(dispatcher: Dispatcher) -> None:
    [i.register(dispatcher) for i in commands]
    menu_commands = [i.create_bot_command() for i in commands if type(i) is Command and i.hint]
    await dispatcher.bot.set_my_commands(menu_commands)


__all__ = ['setup', 'process_check_deadlines']
