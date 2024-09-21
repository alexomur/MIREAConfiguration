from abc import ABC, abstractmethod
from typing import List
from typing import Tuple

class Command(ABC):
    name: str
    aliases: List[str]
    description: str

    @abstractmethod
    def execute(self, arguments: list[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise. Out str - something to print
        """
        pass
