import abc
import typing
from vbml.utils import ContextInstanceMixin


class AbstractValidator(metaclass=abc.ABCMeta):
    key = None  # unique key of validator by which it can be called.


class AbstractSyncValidator(AbstractValidator):
    def check(self, text: str, *args) -> typing.Union[typing.Any, None]:
        ...

    def __call__(self, *args, **kwargs):
        return self.check(*args, **kwargs)


class AbstractAsynchronousValidator(AbstractValidator):
    async def check(self, text: str, *args) -> typing.Union[typing.Any, None]:
        ...

    async def __call__(self, *args, **kwargs):
        return await self.check(*args, **kwargs)


AnyValidator = typing.TypeVar(
    "AnyValidator", AbstractSyncValidator, AbstractAsynchronousValidator
)


class ValidatorManager(ContextInstanceMixin):
    def __init__(self, validators: typing.List[AnyValidator] = None):
        if validators is None:
            validators: typing.List[AnyValidator] = []
        self._validators: dict = {}
        for validator in validators:
            self.add_validator(validator)

        self.set_current(self)

    @property
    def validators(self) -> typing.Dict:
        return self._validators

    def _validate_validator(self, validator: AnyValidator):
        if validator.key is None or not isinstance(validator.key, str):
            raise RuntimeError(f"Unallowed key for validator ({validator.key})")
        exist = self._validators.get(validator.key)
        if exist:
            raise RuntimeError(f"Validator manager have already this key ({exist!r})")

    def add_validator(self, validator: AnyValidator) -> None:
        self._validate_validator(validator)
        self.validators.update({validator.key: validator})

    def get_validator(self, key: str) -> AnyValidator:
        validator = self.validators.get(key)
        if not validator:
            raise RuntimeError("Unknown validator")
        return validator
