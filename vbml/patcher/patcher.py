from .pattern import Pattern
from .loader import Loader
from inspect import iscoroutinefunction
from typing import Optional
import asyncio
from ..validators import ValidatorManager
from .standart import PatchedValidators
from ..utils import ContextInstanceMixin


class Patcher(ContextInstanceMixin):
    def __init__(
        self,
        disable_validators: bool = False,
        manager: ValidatorManager = None,
        **pattern_context
    ):
        self.disable_validators = disable_validators
        self.pattern_context = pattern_context
        self.manager = manager or ValidatorManager.get_current()
        self.set_current(self)

    def add_manager(self, manager: ValidatorManager) -> None:
        self.manager = manager

    def pattern(self, text: str, **context):
        context.update(self.pattern_context)
        return Pattern(text, **context)

    def loader(
        self, arguments_creation_mode: int = 1, use_validators: bool = False, **context
    ) -> Loader:
        context.update(self.pattern_context)
        return Loader(arguments_creation_mode, use_validators, **context)

    async def check_async(
        self, text: str, pattern: Pattern, ignore_features: bool = False
    ):
        if ignore_features:
            return pattern(text)
        return await self._check(text, pattern)

    def check(self, text: str, pattern: Pattern, ignore_features: bool = False):
        if ignore_features:
            return pattern(text)
        loop = asyncio.get_event_loop()
        if loop.is_running():
            raise RuntimeError("Please `check_async` when loop is running.")
        return loop.run_until_complete(self._check(text, pattern))

    async def _check(
        self, text: str, pattern: Pattern, ignore_validation: bool = False
    ):
        if self.manager is None:
            raise RuntimeError("Configure `ValidatorManager` for work with Patcher.")

        check = pattern(text)

        if ignore_validation:
            return check

        if not check:
            return None

        keys = pattern.dict()

        if self.disable_validators:
            return keys

        valid_keys: Optional[dict] = {}

        for key in keys:
            if valid_keys is None:
                break
            if key in pattern.validation:
                for validator in pattern.validation[key]:

                    validator_class = self.manager.get_validator(validator)
                    args = pattern.validation[key][validator] or []

                    if self.manager.patched is None:
                        if iscoroutinefunction(validator_class.check):
                            valid = await validator_class(keys[key], *args)
                        else:
                            valid = validator_class(keys[key], *args)
                    else:
                        valid = await self.manager.patched[validator](keys[key], *args)

                    if valid is None:
                        valid_keys = None
                        break
                    else:
                        valid_keys[key] = valid

            elif valid_keys is not None:
                valid_keys[key] = keys[key]

        pattern.set_dict(valid_keys)

        return valid_keys
