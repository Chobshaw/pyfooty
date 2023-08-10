from abc import ABC, abstractmethod
import hashlib
from collections.abc import Iterable
from typing import Protocol

from attrs import frozen

from entities.dict_mixin import DictMixin


def get_deterministic_hash(item: str) -> int:
    return int(hashlib.md5(item.encode('utf-8')).hexdigest()[:15], base=16)


@frozen
class EntityOld(ABC):
    @property
    @abstractmethod
    def unique_id_attributes(cls) -> Iterable[str]:
        ...

    @property
    def id(self) -> int:
        id_string = '_'.join(self.unique_id_attributes)
        return get_deterministic_hash(id_string)


class Entity(DictMixin):
    ...
