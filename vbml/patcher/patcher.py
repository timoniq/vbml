from .pattern import Pattern
from .exceptions import ValidationError
from inspect import getmembers, ismethod, iscoroutinefunction
from ..validators import standart
from typing import Optional, ClassVar, Callable
from asyncio import AbstractEventLoop, get_event_loop


def get_validators_from_class(validators, validators_kwargs: dict = None) -> dict:
    members_tuple = getmembers(
        validators(**validators_kwargs if validators_kwargs else {}),
        predicate=ismethod,
    )
    return dict((x, y) for x, y in members_tuple if not x.startswith("__"))


async def coroutine_independency(func: Callable, args: tuple = None, kwargs: dict = None):
    if iscoroutinefunction(func):
        return await func(*(args or ()), **(kwargs or {}))
    return func(*(args or ()), **(kwargs or {}))


class Patcher:
    def __init__(self, validators: ClassVar = None, disable_validators: bool = False, **context):
        self.__validators = get_validators_from_class(validators or standart.VBMLValidators, context)
        self.disable_validators = disable_validators
        self.prefix = []
        self.loop: AbstractEventLoop = context.get("loop", get_event_loop())

    def pattern(self, text: str, **context):
        return Pattern(text, prefix=self.prefix, **context)

    def check(self, text: str, pattern: Pattern, ignore_features: bool = False):
        if ignore_features:
            return pattern(text)
        return self.__check_validators__(text, pattern)

    def __check_validators__(self, text: str, pattern: Pattern):
        check = pattern(text)

        if not check:
            return False

        keys = pattern.dict()

        if self.disable_validators:
            return keys

        valid_keys: Optional[dict] = {}

        for key in keys:
            if key in pattern.validation:
                for validator in pattern.validation[key]:

                    if validator not in self.__validators:
                        raise ValidationError(f"Validator <:{validator}> is undefined!")

                    valid = self.loop.run_until_complete(
                        coroutine_independency(
                            self.__validators[validator],
                            args=(keys[key]),
                            kwargs=pattern.validation[key][validator])
                    )

                    if valid is None:
                        valid_keys = None
                        break
                    else:
                        valid_keys[key] = valid

            else:
                valid_keys[key] = keys[key]

        pattern.set_dict_after_patcher_check(valid_keys)

        return valid_keys

