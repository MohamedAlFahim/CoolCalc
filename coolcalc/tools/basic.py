import re
from decimal import Decimal

SCI_NOT_PATTERN = re.compile(r'^(-?[1-9]\.?\d*)[EeXx](10\^)?([+\-]?\d+)$')


def check_scientific_notation(value: str):
    sci_not_match = SCI_NOT_PATTERN.findall(value)
    if (not sci_not_match) or (abs(Decimal(sci_not_match[0][0])) > Decimal('10.')):  # Only normalized form accepted
        return None
    coefficient = Decimal(sci_not_match[0][0])
    exponent = Decimal(sci_not_match[0][-1])
    return coefficient, exponent


def compute_scientific_notation(value: str):
    check_result = check_scientific_notation(value)
    if check_result is None:
        raise Exception('Improper scientific notation')  # Will be changed to a custom exception later
    return Decimal(check_result[0] * (Decimal('10.') ** check_result[1]))


def basic_is_integer(value: Decimal):
    return value == Decimal(int(value))


def is_integer(value: str):
    value = value[1:] if (value[0] == '-') else value
    result = value
    try:
        result = compute_scientific_notation(value)
        return basic_is_integer(result)
    except Exception:
        return basic_is_integer(Decimal(result))


def convert_to_scientific_notation():
    pass
