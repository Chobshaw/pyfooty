from collections.abc import Mapping
import dataclasses
from enum import Enum, EnumType
import inspect
from types import NoneType
from typing import Any, NamedTuple, Optional, Self, get_type_hints
import warnings

import attrs


def has_dict_mixin(obj: Any) -> bool:
    return issubclass(obj, DictMixin) or isinstance(obj, DictMixin)


def is_enum(obj: Any) -> bool:
    return issubclass(obj, Enum) or isinstance(obj, Enum)


def get_enum(val: Any, enum_cls: EnumType) -> Enum:
    try:
        return enum_cls(val)
    except ValueError as exception:
        return enum_cls[val]
    except KeyError:
        raise exception


class Field(NamedTuple):
    name: str
    value: Any = None
    type: Optional[type] = None


def instance_dict(instance: Any) -> dict[str, Any]:
    if dataclasses.is_dataclass(instance):
        return dataclasses.asdict(instance)
    if attrs.has(instance):
        return attrs.asdict(instance)
    return vars(instance)


def _class_fields_dict(cls: type) -> dict[str, Field]:
    type_hints = get_type_hints(cls)
    if hasattr(cls, '__init__'):
        for key, val in inspect.signature(
            getattr(cls, '__init__')
        ).parameters.items():
            if key == 'self' or key in type_hints:
                continue
            type_hints[key] = (
                val.annotation if val.annotation != inspect._empty else None
            )
    return {
        name: Field(name=name, type=type_hint)
        for name, type_hint in type_hints.items()
    }


def _instance_fields_dict(cls: Any) -> dict[str, Field]:
    cls_dict = instance_dict(cls)
    return {
        name: Field(name=name, value=value, type=type(value))
        for name, value in cls_dict.items()
    }


def fields_dict(cls: type | Any) -> dict[str, Field]:
    if isinstance(cls, type):
        return _class_fields_dict(cls)
    return _instance_fields_dict(cls)


class DictMixin:
    @staticmethod
    def _get_attribute(field_val: Any, field_type: type) -> Any:
        if field_type is NoneType and field_val is not None:
            raise TypeError(
                f'Value: {field_val}, cannot be coerced to type: NoneType'
            )
        if isinstance(field_val, field_type):
            return field_val
        if hasattr(field_type, '__args__'):
            for arg in field_type.__args__:
                try:
                    return DictMixin._get_attribute(field_val, arg)
                except TypeError:
                    continue
        if has_dict_mixin(field_type):
            return field_type.from_dict(field_val)
        if is_enum(field_type):
            return get_enum(field_val, field_type)
        if isinstance(field_val, Mapping):
            return field_type(**field_val)
        return field_type(field_val)

    @classmethod
    def from_dict(cls, obj: Mapping) -> Self:
        fields = fields_dict(cls)
        attributes = {}
        for attr_name, attr_val in obj.items():
            field = fields.get(attr_name)
            if field is None:
                warnings.warn(
                    f'Key: {attr_name}, '
                    f'not a recognised field in class: {cls.__name__}. '
                    'Remove this key from input to avoid this warning.',
                    RuntimeWarning,
                )
                continue
            attributes[attr_name] = cls._get_attribute(attr_val, field.type)
        return cls(**attributes)

    def to_dict(self) -> dict:
        return instance_dict(self)
