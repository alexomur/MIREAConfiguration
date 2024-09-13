from .command_abc import Command
import typing
import __main__ as main

class Exit(Command):
    name: str = "exit"
    aliases = []
    description: str = "Stops the application"

    def execute(self, arguments: list[str]) -> typing.NoReturn:
        main.set_exiting(True)
