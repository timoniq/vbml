from .pattern import Pattern
from .loader import Loader
import typing
from .standart import PatchedValidators
from ..utils import ContextInstanceMixin


class Patcher(ContextInstanceMixin):
    def __init__(
        self,
        disable_validators: bool = False,
        validators: typing.Type[PatchedValidators] = None,
        default_validators: typing.List[str] = None,
        **pattern_inherit_context,
    ):
        self.disable_validators, self.default_validators = disable_validators, default_validators
        self.pattern_context = pattern_inherit_context
        self.validators = validators() if validators else PatchedValidators()
        self.set_current(self)

    def pattern(self, _pattern: typing.Union[str, Pattern], **context):
        context.update(self.pattern_context)
        if isinstance(_pattern, Pattern):
            return _pattern.context_copy(**context)
        return Pattern(_pattern,
                       default_validators=self.default_validators,
                       **context)

    def loader(
        self, arguments_creation_mode: int = 1, use_validators: bool = False, **context
    ) -> Loader:
        context.update(self.pattern_context)
        return Loader(arguments_creation_mode, use_validators, **context)

    def check(
        self,
        text: str,
        pattern: Pattern,
        ignore_validation: bool = False,
        ignore_features: bool = False,
    ):
        if ignore_features:
            return pattern(text)

        check = pattern(text)

        if ignore_validation:
            return check

        if not check:
            return None

        keys = pattern.dict()

        if self.disable_validators:
            return keys

        valid_keys: typing.Optional[dict] = {}

        for key in keys:
            if valid_keys is None:
                break
            if key in pattern.validation:
                for validator in pattern.validation[key]:
                    validator_obj = self.validators._find_validator(validator)
                    if validator_obj is None:
                        raise ValueError(f"Unknown validator: {validator}")

                    args = pattern.validation[key][validator] or []
                    valid = self.validators._find_validator(validator)(keys[key], *args)

                    if valid is None:
                        valid_keys = None
                        break
                    else:
                        valid_keys[key] = valid

            elif valid_keys is not None:
                valid_keys[key] = keys[key]

        pattern.set_dict(valid_keys)

        return valid_keys
