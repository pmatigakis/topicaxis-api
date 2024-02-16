from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
P = TypeVar("P")


class Mapper(ABC, Generic[T, P]):
    @abstractmethod
    def map(self, item: T) -> P:
        ...
