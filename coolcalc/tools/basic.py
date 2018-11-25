import re
from decimal import Decimal
from coolcalc.exceptions.basic import ImproperScientificNotation

STRICT_SCI_NOT_PATTERN = re.compile(r'^(-?[1-9](\.\d*)?)[EeXx](10\^)?([+\-]?\d+)$')
ACCEPTING_SCI_NOT_PATTERN = re.compile(r'^(-?\d*\.?\d*)[EeXx](10\^)?([+\-]?\d*\.?\d*)$')


def check_scientific_notation(value: str, strict=True):
    sci_not_match = STRICT_SCI_NOT_PATTERN.findall(value) if strict else ACCEPTING_SCI_NOT_PATTERN.findall(value)
    if not sci_not_match:
        return None
    coefficient = Decimal(sci_not_match[0][0])
    exponent = Decimal(sci_not_match[0][-1])
    return coefficient, exponent


def compute_scientific_notation(value: str):
    check_result = check_scientific_notation(value)
    if check_result is None:
        raise ImproperScientificNotation(value)
    return Decimal(check_result[0] * (Decimal('10.') ** check_result[1]))


def basic_is_integer(value: Decimal):
    return value == Decimal(int(value))


def is_integer(value: str):
    value = value[1:] if (value[0] == '-') else value
    result = value
    try:
        result = compute_scientific_notation(value)
        return basic_is_integer(result)
    except ImproperScientificNotation:
        return basic_is_integer(Decimal(result))


def convert_to_scientific_notation(value: str):
    pass
