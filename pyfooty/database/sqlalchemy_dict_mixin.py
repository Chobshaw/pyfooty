from typing import Any, Optional, Self, get_type_hints
from collections.abc import Mapping
import warnings

from attrs import define, field
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    ColumnProperty,
    Relationship,
    Composite,
)


class MissingForeignKeyDictMixinError(AttributeError):
    def __init__(self, obj: Any) -> None:
        super().__init__(
            f'{obj.__name__} object has no attribute "from_dict". '
            'All foreign key classes must also have '
            'the SqlAlchemyDictMixin or define a "from_dict" method.'
        )


Property = ColumnProperty | Relationship | Composite


@define
class Field:
    name: str
    value: Any = field(default=None)
    type: Optional[type] = field(default=None)
    property: Optional[Property] = field(default=None)


def _get_class_fields_dict(
    cls: type[DeclarativeBase], *, include_composites: bool = False
) -> dict[str, Field]:
    type_hints = get_type_hints(cls)

    composite_field_components = []

    fields_dict = {}
    for name, type_hint in type_hints.items():
        property = getattr(cls, name).property
        if isinstance(property, Composite):
            composite_field_components.extend(property.attrs)
        fields_dict[name] = Field(name, type=type_hint, property=property)

    if not include_composites:
        for name in composite_field_components:
            fields_dict.pop(name)

    return fields_dict


def _get_instance_fields_dict(
    instance: DeclarativeBase, *, include_composites: bool = False
) -> dict[str, Field]:
    fields_dict = _get_class_fields_dict(
        instance.__class__, include_composites=include_composites
    )
    for name, field in fields_dict.items():
        field.value = getattr(instance, name)
    return fields_dict


def get_fields_dict(
    obj: type | Any, *, include_composites: bool = False
) -> dict[str, Field]:
    if isinstance(obj, type):
        return _get_class_fields_dict(
            obj, include_composites=include_composites
        )
    return _get_instance_fields_dict(obj, include_composites=include_composites)


def _get_foreign_key_col(property: Property) -> Column:
    if len(property.local_columns) > 1:
        warnings.warn(
            f'More than one local column present for column: {property.key}. '
            'This could cause unexpected behaviour.',
            RuntimeWarning,
        )
    return next(iter(property.local_columns))


def _get_foreign_key(column: Column) -> ForeignKey:
    if len(column.foreign_keys) > 1:
        warnings.warn(
            'More than one foreign key present '
            f'for column: {column.name}. '
            'This could cause unexpected behaviour.',
            RuntimeWarning,
        )
    return next(iter(column.foreign_keys))


class SqlAlchemyDictMixin:
    @staticmethod
    def _get_field_from_relationship(attr_val: Any, field: Field):
        foreign_key_col = _get_foreign_key_col(field.property)
        foreign_key = _get_foreign_key(foreign_key_col)
        foreign_key_id = (
            attr_val.get(foreign_key.column.name)
            if isinstance(attr_val, dict)
            else getattr(attr_val, foreign_key.column.name, None)
        )
        if foreign_key_id is not None:
            return Field(foreign_key_col.name, value=foreign_key_id)

        foreign_key_cls = field.property.entity.class_
        if isinstance(attr_val, dict):
            try:
                return Field(
                    field.name,
                    value=foreign_key_cls.from_dict(attr_val),
                )
            except AttributeError as exception:
                raise MissingForeignKeyDictMixinError(foreign_key_cls)
        try:
            return Field(
                field.name,
                value=foreign_key_cls.from_dict(attr_val.to_dict(deep=False)),
            )
        except AttributeError as exception:
            raise MissingForeignKeyDictMixinError(foreign_key_cls)
        except TypeError as exception:
            raise exception(
                'All inputs for foreign key classes must either '
                'be of type: dict, or define a "to_dict" method.'
            )

    @classmethod
    def _get_model_field(cls, attr_val: Any, field: Field):
        if isinstance(field.property, Relationship):
            return cls._get_field_from_relationship(attr_val, field)
        return Field(field.name, value=attr_val)

    @classmethod
    def from_dict(cls, obj: Mapping) -> Self:
        fields_dict = get_fields_dict(cls)

        model_attrs = {}
        for attr_name, attr_val in obj.items():
            field = fields_dict.get(attr_name)
            if field is None:
                warnings.warn(
                    f'Key: {attr_name}, '
                    f'not a recognised field in class: {cls.__name__}. '
                    'Remove this key from input to avoid this warning.',
                    RuntimeWarning,
                )
                continue
            new_field = cls._get_model_field(attr_val=attr_val, field=field)
            model_attrs[new_field.name] = new_field.value

        return cls(**model_attrs)

    def to_dict(self) -> dict[str, Any]:
        fields_dict = get_fields_dict(self)
        return {name: field.value for name, field in fields_dict.items()}
