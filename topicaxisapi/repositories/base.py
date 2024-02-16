from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from topicaxisapi.repositories.filters import Filters

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def list(
        self,
        offset: int = 0,
        limit: int = 10,
        filters: Filters | None = None,
    ) -> list[T]:
        ...

    @abstractmethod
    def save(self, model: T) -> T:
        ...

    @abstractmethod
    def save_bulk(self, models: List[T]):
        ...

    @abstractmethod
    def delete(self, model: T):
        ...
