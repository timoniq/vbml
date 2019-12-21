from typing import TypeVar, Type
from inspect import getmembers, ismethod

import contextvars

T = TypeVar("T")


class ContextInstanceMixin:
    """
    Author: https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/utils/mixins.py
    """

    def __init_subclass__(cls, **kwargs):
        cls.__context_instance = contextvars.ContextVar("instance_" + cls.__name__)
        return cls

    @classmethod
    def get_current(cls: Type[T], no_error=True) -> T:
        if no_error:
            return cls.__context_instance.get(None)
        return cls.__context_instance.get()

    @classmethod
    def set_current(cls: Type[T], value: T):
        if not isinstance(value, cls):
            raise TypeError(
                f"Value should be instance of '{cls.__name__}' not '{type(value).__name__}'"
            )
        cls.__context_instance.set(value)


def class_members(validators, validators_kwargs: dict = None) -> dict:
    members_tuple = getmembers(validators, predicate=ismethod)
    return dict((x, y) for x, y in members_tuple if not x.startswith("__"))
