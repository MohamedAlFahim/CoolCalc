from coolcalc.signals.signal_structure import Signal
from coolcalc.datanodes.terminal.Numerical import RegularNumerical

INVERT_SIGN_SIGNAL = Signal('invert sign')


class Inverter:
    def __init__(self, child_1, child_2):
        self.children = [child_1, child_2]
        self.signal = INVERT_SIGN_SIGNAL

    def act(self):
        print(self.children[0].value)
        print(self.children[1].value)
        self.signal.propagate_to_children(self.children)
        print(self.children[0].value)
        print(self.children[1].value)


x = Inverter(RegularNumerical('2'), RegularNumerical('-3'))
x.act()
