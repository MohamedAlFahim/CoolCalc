from coolcalc.datanodes.terminal.Terminal import Terminal
from abc import abstractmethod


class Numerical(Terminal):
    @abstractmethod
    def __init__(self, value: str):
        raise NotImplementedError()


class RegularNumerical(Numerical):
    def __init__(self, value: str):
        pass

    def handle_signal(self, signal):
        pass

    @property
    def latex(self, *args):
        pass
