import click

from topicaxisapi.cli.commands.articles import articles_cli
from topicaxisapi.cli.commands.users import users_cli


@click.group()
def main():
    pass


main.add_command(articles_cli)
main.add_command(users_cli)
