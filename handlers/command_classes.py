from dataclasses import dataclass, field
from typing import Callable, Optional, Union, Awaitable, Any

from aiogram.dispatcher.filters.state import State
from aiogram import Dispatcher
from aiogram.types import ContentTypes, Message, BotCommand


@dataclass
class ABCCommand:
    process: Callable[[Message], Awaitable[Any]]

    def register(self, dispatcher: Dispatcher) -> None:
        pass


@dataclass
class Command(ABCCommand):
    commands: Union[list[str], str]
    hint: str

    def register(self, dispatcher: Dispatcher) -> None:
        dispatcher.register_message_handler(
            callback=self.process,
            commands=self.commands,
            state='*'
        )

    def create_bot_command(self) -> BotCommand:
        command: str
        if type(self.commands) is str:
            command = self.commands
        else:
            command = self.commands[0]
        return BotCommand(command=command, description=self.hint)


@dataclass
class StateCommand(ABCCommand):
    state: Optional[State]
    content_types: Optional[ContentTypes]

    def register(self, dispatcher: Dispatcher) -> None:
        dispatcher.register_message_handler(
            callback=self.process,
            state=self.state,
            content_types=self.content_types
        )
