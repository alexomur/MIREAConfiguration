from abc import ABC, abstractmethod, abstractproperty


class Command(ABC):
    name: str
    aliases: list[str]
    description: str

    @abstractmethod
    def execute(self, arguments: list[str]) -> bool:
        pass