from coolcalc.datanodes.terminal.Terminal import Terminal
from abc import abstractmethod
from coolcalc.tools.basic import remove_negative_sign
from coolcalc.tools.basic import check_scientific_notation
from coolcalc.preferences import HIGHLIGHT_COLOR
from coolcalc.tools.latex import color


class Numerical(Terminal):
    @abstractmethod
    def __init__(self, value: str):
        raise NotImplementedError()

    def fits(self, targets):
        return 'numerical' in targets


class RegularNumerical(Numerical):
    def __init__(self, value: str):
        self.value = value

    def handle_signal(self, signal):
        signal_content = signal.content
        without_sign, has_negative_sign = remove_negative_sign(self.value)
        if signal_content == 'invert sign':
            if has_negative_sign:
                self.value = without_sign
            else:
                self.value = '-' + self.value
        elif signal_content == 'absolute value':
            self.value = without_sign
        else:
            raise Exception('The signal content', signal_content, 'is not recognized.')

    def latex(self, *args):
        check_result = check_scientific_notation(self.value)
        if check_result is None:
            return str(self.value)
        coefficient = check_result[0]
        exponent = check_result[1]
        if 'highlight coefficient' in args:
            coefficient = color(HIGHLIGHT_COLOR, coefficient)
        if 'highlight exponent' in args:
            exponent = color(HIGHLIGHT_COLOR, exponent)
        return f'{coefficient} \\times 10^{{{exponent}}}'

    def fits(self, targets):
        return (super().fits(targets)) or ('regular numerical' in targets)
