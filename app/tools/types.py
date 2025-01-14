from typing import Annotated, TypeVar

from decimal import Decimal, InvalidOperation

from pydantic import AfterValidator, ValidationError


T = TypeVar('T')


def validate_positive_2_scale(value: T) -> T:
    try:
        if value.as_tuple().exponent < -2:
            raise ValueError(
                "Value must not have more than 2 decimal places"
            )
        if value < 0:
            raise ValueError(
                "Value must be positive"
            )
        return value
    except InvalidOperation:
        raise ValueError("Invalid decimal number")


Positive2DecimalPlaces = Annotated[Decimal, AfterValidator(validate_positive_2_scale)]
