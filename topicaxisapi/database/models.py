from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Index,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    literal,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import TypeDecorator


class Base(DeclarativeBase):
    pass


class TSVector(TypeDecorator):
    impl = TSVECTOR


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[str] = mapped_column(String(40), nullable=False)
    url: Mapped[str] = mapped_column(Text(), nullable=False)
    title: Mapped[str] = mapped_column(Text(), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    image: Mapped[str] = mapped_column(Text(), nullable=True)
    summary: Mapped[str] = mapped_column(Text(), nullable=True)
    source: Mapped[dict] = mapped_column(JSONB(), nullable=False)
    categories: Mapped[list] = mapped_column(JSONB(), nullable=False)
    tags: Mapped[list] = mapped_column(JSONB(), nullable=False)
    channels: Mapped[list] = mapped_column(JSONB(), nullable=False)
    keywords: Mapped[list] = mapped_column(JSONB(), nullable=False)
    named_entities: Mapped[list] = mapped_column(JSONB(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_articles_id"),
        Index(
            "ix_articles_title_tsv",
            func.to_tsvector(literal("english"), title),
            postgresql_using="gin",
        ),
        Index(
            "ix_articles_summary_tsv",
            func.to_tsvector(literal("english"), summary),
            postgresql_using="gin",
        ),
        Index("ix_articles_updated_at_id_desc", updated_at.desc(), id.desc()),
        Index(
            "ix_articles_channels",
            "channels",
            postgresql_using="gin",
        ),
        Index(
            "ix_articles_tags",
            "tags",
            postgresql_using="gin",
        ),
        Index(
            "ix_articles_categories",
            "categories",
            postgresql_using="gin",
        ),
        Index(
            "ix_articles_source",
            "source",
            postgresql_using="gin",
        ),
    )


class Category(Base):
    __tablename__ = "categories"

    __table_args__ = (PrimaryKeyConstraint("id", name="pk_categories_id"),)

    id: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    taxonomy: Mapped[dict] = mapped_column(JSONB(), nullable=False)


class Channel(Base):
    __tablename__ = "channels"

    __table_args__ = (PrimaryKeyConstraint("id", name="pk_channels_id"),)

    id: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    url: Mapped[str] = mapped_column(Text(), nullable=False)


class Tag(Base):
    __tablename__ = "tags"

    __table_args__ = (PrimaryKeyConstraint("id", name="pk_tags_id"),)

    id: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(40), nullable=False)


class Source(Base):
    __tablename__ = "sources"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_sources_id"),
        Index(
            "ix_sources_name",
            "name",
        ),
    )

    id: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(Text(), nullable=False)
    url: Mapped[str] = mapped_column(Text(), nullable=False)


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_users_id"),
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("api_key", name="uq_users_api_key"),
        Index(
            "ix_users_api_key",
            "api_key",
        ),
    )

    id: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(40), nullable=False)
    api_key: Mapped[str] = mapped_column(String(40), nullable=False)
