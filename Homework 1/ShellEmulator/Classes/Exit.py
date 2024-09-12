from .Command import Command
import typing

class Exit(Command):
    name: str = "exit"
    aliases = []
    description: str = "Stops the application"

    def execute(self, arguments: list[str]) -> typing.NoReturn:
        exit(0)
