from abc import ABC, abstractmethod
from typing import List

class Command(ABC):
    name: str
    aliases: List[str]
    description: str

    @abstractmethod
    def execute(self, arguments: list[str]) -> bool:
        pass