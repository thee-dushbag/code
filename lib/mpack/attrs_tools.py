from typing import Any, Callable

from attrs import Attribute, AttrsInstance, define, field
from mpack import print

_Validator = Callable[[AttrsInstance, Attribute, Any], Any]
_SelfValidator = Callable[[Any, AttrsInstance, Attribute, Any], Any]


@define(frozen=True, slots=True)
class InitValidator:
    validator: _Validator | _SelfValidator
    pass_self: bool = field(default=False, kw_only=True)

    def __call__(self, __self__, inst, attr, value) -> Any:
        if self.pass_self:
            attrs = __self__, inst, attr, value
        else:
            attrs = inst, attr, value
        return self.validator(*attrs)


class AttrsFieldValidator:
    def __validate(self, attr_inst, attr, value):
        validator: _Validator = getattr(self, attr.name, self.__no_validator)
        return validator(attr_inst, attr, value)

    def validate(self, attr_inst, attr, value):
        return self.__validate(attr_inst, attr, value)

    def __no_validator(self, attrs_inst, attr, value):
        raise ValidatorNotFound(attr.name, value, self)

    def __call__(self, attr_inst, attr, value) -> Any:
        return self.__validate(attr_inst, attr, value)


class FieldValidator(AttrsFieldValidator):
    ...


_Validators = InitValidator | _Validator | _SelfValidator


class AttrsFieldInitValidator(AttrsFieldValidator):
    def __init__(self, **validators: _Validators) -> None:
        for name, validator in validators.items():
            validator = self._get_validator(validator)
            setattr(self, name, self._init_validator(validator))

    def _get_validator(self, validator: _Validators) -> InitValidator:
        if isinstance(validator, InitValidator):
            return validator
        _ps1 = "__self__" in validator.__code__.co_varnames
        _ps2 = getattr(validator, "pass_self", False)
        pass_self = _ps1 or _ps2
        return InitValidator(validator, pass_self=pass_self)

    def _init_validator(self, validator: InitValidator):
        def _pass_self_validator(__self__, validator):
            def _validate_interface(inst, attr, value):
                return validator(__self__, inst, attr, value)

            return _validate_interface

        return _pass_self_validator(self, validator)


class ValidationError(Exception):
    def __init__(self, attr_name, attr_value, validator, message=None) -> None:
        self.attr_name = attr_name
        self.attr_value = attr_value
        self.validator = validator
        self.message = message or ""


class ValidatorNotFound(ValidationError):
    def __str__(self):
        return (
            f"No Validator for {self.attr_name}={self.attr_value!r} in {self.validator}"
        )


class ValidationFailure(ValidationError):
    def __str__(self):
        return f"Failed Validating {self.attr_name!r} set to {self.attr_value!r} in {self.validator}: REASON: {self.message}"
