from coolcalc.tools.basic import get_decimal_position, check_scientific_notation, remove_negative_sign
from decimal import Decimal

result = []
zeros_put_aside = []
significant_digit_left = False


# Rule Numbers
NON_ZERO_RULE = 1  # Non-zero digits are significant
ZEROS_BETWEEN_RULE = 2  # Zeros between significant digits are significant
LESS_THAN_ONE_RULE = 3  # For numbers less than 1 (i.e. 0.0010), the rightmost end digits are significant. In other
# words, all digits except the beginning zeros (i.e. 0.00000...) are significant.
GREATER_THAN_OR_EQUAL_TO_ONE_RULE = 4  # For numbers greater than or equal to 1, all digits except the leading zeros
# are significant.


def add_significant_digit(digit: str, position: int, rule: int):
    result.append((digit, position, rule))
    global significant_digit_left
    significant_digit_left = True


def collect_zeros_put_aside():
    global zeros_put_aside
    for zero_position in zeros_put_aside:
        add_significant_digit('0', zero_position, ZEROS_BETWEEN_RULE)
    zeros_put_aside = []


def cleanup():
    global result
    global zeros_put_aside
    global significant_digit_left
    result = []
    zeros_put_aside = []
    significant_digit_left = False


def count_negative_sign_offset(value: str):
    without_sign, has_negative_sign = remove_negative_sign(value)
    return without_sign, int(has_negative_sign)


def count_leading_zeros_offset(value: str):
    original_length = len(value)
    without_leading_zeros = value.lstrip('0')
    return without_leading_zeros, original_length - len(without_leading_zeros)


def handle_sig_fig_info_without_point(value: str):
    without_sign, negative_sign_offset = count_negative_sign_offset(value)
    without_leading_zeros, leading_zeros_offset = count_leading_zeros_offset(without_sign)
    offset = negative_sign_offset + leading_zeros_offset
    global significant_digit_left
    i = 0
    for character in without_leading_zeros:
        if character == '0':
            if significant_digit_left:
                zeros_put_aside.append(i + offset)
        else:
            significant_digit_left = True
            add_significant_digit(character, i + offset, NON_ZERO_RULE)
            collect_zeros_put_aside()
        i += 1
    temp = result
    cleanup()
    return temp


def handle_sig_fig_info_with_point(value: str):
    without_sign, negative_sign_offset = count_negative_sign_offset(value)
    without_leading_zeros, leading_zeros_offset = count_leading_zeros_offset(without_sign)
    offset = negative_sign_offset + leading_zeros_offset
    global significant_digit_left
    i = 0
    if Decimal(without_leading_zeros) < 1:
        without_point = without_leading_zeros[1:]
        offset += 1
        while without_point[i] == '0':
            i += 1
        for character in without_point[i:]:
            add_significant_digit(character, i + offset, LESS_THAN_ONE_RULE)
            i += 1
    else:
        for character in without_leading_zeros:
            if character != '.':
                add_significant_digit(character, i + offset, GREATER_THAN_OR_EQUAL_TO_ONE_RULE)
            i += 1
    temp = result
    cleanup()
    return temp


def significant_figure_info(value: str):
    check_result = check_scientific_notation(value)
    if check_result is not None:  # scientific notation
        value, exponent = check_result
        value = str(value)
    if Decimal(value) == 0:
        return []  # Note that 0, 0., 0.0, 0.00, and etc. have no sig-figs.
    if get_decimal_position(value) is None:
        return handle_sig_fig_info_without_point(value)
    return handle_sig_fig_info_with_point(value)


# Note that character positions, rather than digit positions, are returned. This is to help with LaTeX underline
# positioning later on (for when the calculator shows its work).

# Test
dictionary = {
    '2220': 3,
    '-0020.': 2,
    '00000.000110': 3,
    '20': 1,
    '0.0': 0,
    '2.0': 2,
    '2.0e1': 2,
    '0.00008': 1
}
for key in dictionary:
    print(significant_figure_info(key))
    print(len(significant_figure_info(key)) == dictionary[key])
    print(' ')
