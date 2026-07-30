from abc import ABC, abstractmethod


class Plugin(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs):
        pass