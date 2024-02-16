import click
from click import ClickException, Group
from sqlalchemy.exc import SQLAlchemyError

from topicaxisapi.cli.resources.database import Database
from topicaxisapi.repositories.sqlalchemy.users import SQLAlchemyUserRepository
from topicaxisapi.services.users.create_user.service import CreateUser
from topicaxisapi.services.users.delete_user.service import DeleteUser
from topicaxisapi.services.users.exceptions import UnknownUserError
from topicaxisapi.services.users.get_user_api_key.service import GetUserApiKey
from topicaxisapi.services.users.reset_api_key.service import ResetApiKey

users_cli = Group("users", help="User management commands")


@users_cli.command("create", help="Create a user")
@click.argument("username")
def create(username):
    with Database() as db:
        session = db.session
        user_repository = SQLAlchemyUserRepository(session)
        create_user = CreateUser(user_repository)
        user = create_user.run(username)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise ClickException("failed to create user") from e

    click.echo(f"api key: {user.api_key}")


@users_cli.command("delete", help="Delete a user")
@click.argument("username")
def delete(username):
    with Database() as db:
        session = db.session
        user_repository = SQLAlchemyUserRepository(session)
        delete_user = DeleteUser(user_repository)
        try:
            delete_user.run(username)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()

            raise ClickException("failed to delete user") from e
        except UnknownUserError as e:
            raise ClickException("user not fount") from e

    click.echo(f"deleted user {username}")


@users_cli.command("reset-api-key", help="Reset a user's api key")
@click.argument("username")
def reset_api_key(username):
    with Database() as db:
        session = db.session
        user_repository = SQLAlchemyUserRepository(session)

        reset_api_key_ = ResetApiKey(user_repository)
        try:
            user = reset_api_key_.run(username)
            session.commit()
            api_key = user.api_key
        except SQLAlchemyError as e:
            session.rollback()

            raise ClickException("failed to reset user's api key") from e
        except UnknownUserError as e:
            raise ClickException("user not fount") from e

    click.echo(f"api key: {api_key}")


@users_cli.command("show-api-key", help="Show a user's api key")
@click.argument("username")
def show_api_key(username):
    with Database() as db:
        session = db.session
        user_repository = SQLAlchemyUserRepository(session)
        get_user_api_key = GetUserApiKey(user_repository)
        try:
            api_key = get_user_api_key.run(username)
        except UnknownUserError as e:
            raise ClickException("user not fount") from e

    click.echo(f"api key: {api_key}")
