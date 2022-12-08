from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, name) -> None:
        self.name = name
        self.run = False

    def get_name(self):
        return self.name

    @abstractmethod
    def start(self, p, n, m):
        pass

    @abstractmethod
    def stop(self):
        self.run = False