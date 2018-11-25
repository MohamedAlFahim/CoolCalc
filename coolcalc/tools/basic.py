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
    sci_not_match = SCI_NOT_PATTERN.findall(value)
    check_result = check_scientific_notation(value)
    if (not sci_not_match) or (abs(Decimal(sci_not_match[0][0])) > Decimal('10.')):  # Only normalized form accepted
        raise Exception('Improper scientific notation')
    coefficient = Decimal(sci_not_match[0][0])
    exponent = Decimal(sci_not_match[0][-1])
    return Decimal(coefficient * (Decimal('10.') ** exponent))


def is_integer(value: str):
    value = value[1:] if (value[0] == '-') else value
    if 'e' in value.lower():
        pass


print(compute_scientific_notation('2.2e-5'))
