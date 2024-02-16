import secrets
from datetime import datetime

from pydantic import BaseModel, Field, validator


class Category(BaseModel):
    id: str
    name: str
    taxonomy: dict = Field(default_factory=dict)


class Categories(BaseModel):
    categories: list[Category]


class Source(BaseModel):
    id: str
    name: str
    url: str


class Tag(BaseModel):
    id: str
    name: str


class ChannelPost(BaseModel):
    posted_at: int
    title: str
    url: str


class Channel(BaseModel):
    id: str
    name: str
    url: str
    posts: list[ChannelPost]


class NamedEntityType(BaseModel):
    id: str
    name: str


class NamedEntity(BaseModel):
    id: str
    value: str
    type: NamedEntityType


class Article(BaseModel):
    id: str
    categories: list[Category]
    created_at: int
    updated_at: int | None = None
    source: Source
    title: str
    url: str
    tags: list[Tag]
    channels: list[Channel]
    description: str | None
    image: str | None
    summary: str | None = None
    keywords: list[str] = Field(default_factory=list)
    named_entities: list[NamedEntity] = Field(default_factory=list)

    @validator("created_at", pre=True)
    def parse_created_at(cls, v):
        if isinstance(v, datetime):
            v = int(v.timestamp())

        return v

    @validator("updated_at", pre=True)
    def parse_updated_at(cls, v):
        if isinstance(v, datetime):
            v = int(v.timestamp())

        return v


class Articles(BaseModel):
    articles: list[Article]


class ChannelDetails(BaseModel):
    id: str
    name: str
    url: str


class Channels(BaseModel):
    channels: list[ChannelDetails]


class Tags(BaseModel):
    tags: list[Tag]


class Sources(BaseModel):
    sources: list[Source]


class User(BaseModel):
    id: int | None = None
    username: str
    api_key: str | None = None

    def reset_api_key(self):
        self.api_key = secrets.token_hex(20)

        return self.api_key
