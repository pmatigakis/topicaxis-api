from click.testing import CliRunner
from faker import Faker

from topicaxisapi.cli.commands.users import (
    create,
    delete,
    reset_api_key,
    show_api_key,
)
from topicaxisapi.database.models import User


def test_create(app_test_session):
    fake = Faker()
    username = fake.user_name()
    runner = CliRunner()
    result = runner.invoke(create, [username], catch_exceptions=False)

    user = app_test_session.query(User).filter(User.username == username).one()

    assert result.exit_code == 0
    assert result.output == f"api key: {user.api_key}\n"


def test_delete(app_test_session, user):
    runner = CliRunner()
    result = runner.invoke(delete, [user.username], catch_exceptions=False)

    assert (
        app_test_session.query(User)
        .filter(User.username == user.username)
        .count()
        == 0
    )
    assert result.exit_code == 0
    assert result.output == f"deleted user {user.username}\n"


def test_reset_api_key(app_test_session, user):
    original_api = user.api_key
    runner = CliRunner()
    result = runner.invoke(
        reset_api_key, [user.username], catch_exceptions=False
    )

    app_test_session.refresh(user)
    assert user.api_key != original_api
    assert result.exit_code == 0
    assert result.output == f"api key: {user.api_key}\n"


def test_show_api_key(app_test_session, user):
    runner = CliRunner()
    result = runner.invoke(
        show_api_key, [user.username], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert result.output == f"api key: {user.api_key}\n"
