import abc
import typing
import inspect
from .utils import ContextInstanceMixin, class_members
from .patcher.standart import PatchedValidators


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
    def __init__(
        self,
        validators: typing.Union[
            typing.List[AnyValidator], AnyValidator, typing.Callable
        ] = None,
    ):
        self._validators: dict = {}
        self._patched: typing.Union[None, dict] = None

        if validators is None:
            validators = []

        if inspect.isclass(validators) and issubclass(validators, PatchedValidators):
            validators = validators()
            patched_validators = class_members(validators)
            self._patched = patched_validators
            self.validators.update(patched_validators)
        else:
            validators = validators if isinstance(validators, list) else [validators]
            for validator in validators:
                self.add_validator(validator)

        self.set_current(self)

    @property
    def validators(self) -> typing.Dict:
        return self._validators

    @property
    def patched(self) -> typing.Union[None, dict]:
        return self._patched

    def _validate_validator(self, validator: AnyValidator):
        if validator.key is None or not isinstance(validator.key, str):
            raise RuntimeError(f"Unallowed key for validator ({validator.key})")
        exist = self._validators.get(validator.key)
        if exist:
            raise RuntimeError(f"Validator manager have already this key ({exist!r})")

    def add_validator(self, validator) -> None:
        self._validate_validator(validator)
        self.validators.update({validator.key: validator})

    def get_validator(self, key: str) -> AnyValidator:
        validator = self.validators.get(key)
        if not validator:
            raise RuntimeError('Unknown validator "{}"'.format(key))
        return validator
