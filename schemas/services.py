from typing import Union

from faker import Faker

fake = Faker()


def get_fake_field(
    col_type: str, start_value: int = None, end_value: int = None
) -> Union[str, int]:
    col_types = {
        "Full name": fake.name,
        "Email": fake.email,
        "Job": fake.job,
        "Company": fake.company,
    }

    # generating int value
    if col_type == "Integer":
        if isinstance(start_value, int) and isinstance(end_value, int):
            if start_value < end_value:
                return fake.pyint(start_value, end_value)
            else:
                raise ValueError('"end_value" must be greater than "start_value"')
        else:
            raise TypeError('"start_value" and "end_value" must be integers')

    # generating all other types
    try:
        return col_types[col_type]()
    except KeyError:
        return fake.name()