from abc import ABC, abstractmethod
from typing import List
from typing import Tuple

class Command(ABC):
    name: str
    aliases: List[str]
    description: str

    @abstractmethod
    def execute(self, arguments: list[str]) -> Tuple[bool, str]:
        pass