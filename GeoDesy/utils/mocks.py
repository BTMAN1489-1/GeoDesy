from collections import namedtuple

__all__ = ("User",)

User = namedtuple("User", ('first_name', 'second_name', 'third_name', 'sex', 'email'))
