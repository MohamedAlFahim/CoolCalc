import re
from decimal import Decimal
from coolcalc.exceptions.basic import ImproperScientificNotation
from coolcalc.preferences import STRICT_SCIENTIFIC_NOTATION

STRICT_SCI_NOT_PATTERN = re.compile(r'^(-?[1-9](\.\d*)?)[EeXx](10\^)?([+\-]?\d+)$')
ACCEPTING_SCI_NOT_PATTERN = re.compile(r'^(-?\d*\.?\d*)[EeXx](10\^)?([+\-]?\d*\.?\d*)$')


def check_scientific_notation(value: str):
    sci_not_match = STRICT_SCI_NOT_PATTERN.findall(
        value) if STRICT_SCIENTIFIC_NOTATION else ACCEPTING_SCI_NOT_PATTERN.findall(value)
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
    result = value
    try:
        result = compute_scientific_notation(value)
        return basic_is_integer(result)
    except ImproperScientificNotation:
        return basic_is_integer(Decimal(result))


def get_decimal_position(value: str):
    point_find_result = value.find('.')
    return point_find_result if (point_find_result != -1) else None


def shift_decimal_left(value: str):
    point_find_result = get_decimal_position(value)
    without_point = value.replace('.', '')
    return without_point[:point_find_result - 1] + '.' + without_point[point_find_result - 1:]


def shift_decimal_right(value: str):
    point_find_result = get_decimal_position(value)
    without_point = value.replace('.', '')
    return without_point[:point_find_result + 1] + '.' + without_point[point_find_result + 1:]


def remove_negative_sign(value: str):
    has_negative_sign = value[0] == '-'
    without_sign = value[1:] if has_negative_sign else value
    return without_sign, has_negative_sign


def handle_less_than_one(value: str):
    shifts = 0
    while Decimal(value) < 1:
        value = shift_decimal_right(value)
        shifts += 1
    coefficient = str(Decimal(value))
    exponent = str(-shifts)
    return coefficient + 'e' + exponent


def handle_greater_than_or_equal_to_ten(value: str):
    shifts = 0
    while Decimal(value) >= 10:
        value = shift_decimal_left(value)
        shifts += 1
    coefficient = str(Decimal(value))
    exponent = str(shifts)
    return coefficient + 'e' + exponent


def convert_to_scientific_notation(value: str):
    check_result = check_scientific_notation(value)
    if check_result is not None:
        return value
    without_sign, has_negative_sign = remove_negative_sign(value)
    point_find_result = value.find('.')
    sign = '-' if has_negative_sign else ''
    if point_find_result == -1:  # No decimal point
        pass
    else:
        if Decimal(without_sign) < 1:  # i.e. 0.0052
            return sign + handle_less_than_one(without_sign)


def get_fractional_part(value: str):
    # Does not work if value is in scientific notation
    point_find_result = get_decimal_position(value)
    if (point_find_result is None) or (value[point_find_result + 1:] == ''):
        return None
    return value[point_find_result + 1:]


def lowest_common_multiple(a: int, b: int):
    from math import gcd
    return int((a * b) / gcd(a, b))


def is_prime(number: int):
    # based on https://stackoverflow.com/questions/567222/simple-prime-generator-in-python
    if number == 0 or number == 1:
        return False
    for divisor in range(2, number):
        if number % divisor == 0:
            return False
    return True


def prime_numbers_until(number: int):
    # also includes 'number' if it is prime
    return list(filter(is_prime, range(1, number + 1)))


def prime_factors(number: int):
    if number == 0:
        raise Exception('Zero has infinite factors.')
    # based on https://en.wikipedia.org/wiki/Talk%3APrime_factorization_algorithm
    primes = []
    candidates = range(2, int(number + 1))
    candidate = 2
    while not primes and candidate in candidates:
        if number % candidate == 0 and is_prime(candidate):
            primes = primes + [candidate] + prime_factors(number/candidate)
        candidate += 1
    return primes
