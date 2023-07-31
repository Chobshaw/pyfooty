from abc import ABC, abstractmethod
import hashlib
from typing import Protocol
from attrs import frozen


def get_deterministic_hash(item: str) -> str:
    return int(hashlib.md5(item.encode('utf-8')).hexdigest()[:16], base=16)


@frozen
class EntityOld(ABC):
    @property
    def id(self) -> str:
        id_string = self._get_id_string()
        return get_deterministic_hash(id_string)

    @abstractmethod
    def _get_id_string(self) -> str:
        ...


class Entity(Protocol):
    ...
