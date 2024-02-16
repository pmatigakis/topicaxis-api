from datetime import datetime

from pydantic import BaseModel


class Filters(BaseModel):
    pass


class ArticleFilters(Filters):
    text: str | None
    categories: list[str] | None
    source: str | None
    tags: list[str] | None
    channels: list[str] | None
    from_date: datetime | None
    to_date: datetime | None
