from dataclasses import dataclass, field
from typing import Callable, Optional, Union
from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State
from aiogram.types import ContentTypes
from state_machine import StateMachine

from .start import process_start
from .subject_commands import process_create_subject, process_delete_subject, \
    process_end_creating_subject, process_end_deleting_subject


@dataclass
class Command:
    process: Callable = field()
    commands: Union[list[str], str, None] = field(default=None)
    state: Optional[State] = field(default=None)
    content_types: Optional[ContentTypes] = field(default=None)

    def register(self, dispatcher: Dispatcher) -> None:
        dispatcher.register_message_handler(
            callback=self.process,
            commands=self.commands,
            state=self.state,
            content_types=self.content_types
        )


commands = [
    Command(process_start, 'start'),
    Command(process_create_subject, 'new_subject'),
    Command(process_delete_subject, 'delete_subject'),
    Command(process_end_creating_subject, state=StateMachine.waiting_for_create_subject, content_types=ContentTypes.TEXT),
    Command(process_end_deleting_subject, state=StateMachine.waiting_for_delete_subject, content_types=ContentTypes.TEXT)
]


def setup(dispatcher: Dispatcher) -> None:
    [i.register(dispatcher) for i in commands]
