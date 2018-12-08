from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def handle_signal(self, signal):
        raise NotImplementedError()

    @abstractmethod
    def fits(self, targets):
        raise NotImplementedError()

    @property
    @abstractmethod
    def latex(self, *args):
        raise NotImplementedError()
