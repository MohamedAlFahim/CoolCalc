from coolcalc.tools.basic import get_decimal_position, check_scientific_notation
from decimal import Decimal


def significant_figure_info(value: str):
    result = []
    zeros_put_aside = []
    significant_digit_left = False
    # 1 - non-zero digits are significant
    # 2 - zeros between two significant digits are significant
    # 3 - if the number has a decimal point, trailing zeros are significant
    check_result = check_scientific_notation(value)
    if check_result is not None:  # scientific notation
        value, exponent = check_result
    if Decimal(value) == 0:
        return []  # Note that 0, 0.0, 0.00, and etc. have no sig-figs.
    point_position = get_decimal_position(value)
    value = value.lstrip('0')
    i = 0
    if point_position is None:  # No decimal point
        for character in value:
            # result.append((digit, position, rule))
            if character == '0':
                pass
            elif character == '.':
                pass
            else:
                result.append((character, i, 1))
            i += 1
