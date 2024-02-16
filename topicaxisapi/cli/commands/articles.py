from logging import getLogger

import click
from click import ClickException, Group
from sqlalchemy.exc import SQLAlchemyError

from topicaxisapi.cli.resources.database import Database
from topicaxisapi.repositories.sqlalchemy.articles import ArticleRepository
from topicaxisapi.repositories.sqlalchemy.categories import CategoryRepository
from topicaxisapi.repositories.sqlalchemy.channels import ChannelRepository
from topicaxisapi.repositories.sqlalchemy.sources import SourceRepository
from topicaxisapi.repositories.sqlalchemy.tags import TagRepository
from topicaxisapi.services.articles.load_articles.service import LoadArticles

logger = getLogger(__name__)
articles_cli = Group("articles", help="Article management commands")


@articles_cli.command("load", help="Load the articles")
@click.argument("articles-file")
def load(articles_file):
    with Database() as db:
        session = db.session
        load_articles = LoadArticles(
            article_repository=ArticleRepository(session),
            category_repository=CategoryRepository(session),
            channel_repository=ChannelRepository(session),
            source_repository=SourceRepository(session),
            tag_repository=TagRepository(session),
        )
        load_articles_result = load_articles.run(articles_file)
        try:
            session.commit()
        except SQLAlchemyError as e:
            logger.exception("failed to create user")
            session.rollback()

            raise ClickException("failed to create user") from e

    click.echo(f"Processed {load_articles_result.lines_processed} lines")
