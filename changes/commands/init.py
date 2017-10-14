import click

from ..models import GitRepository

# def bumpversion_init():
# def towncrier_init():


def index_repository():
    return GitRepository()


def info(message):
    click.echo(click.style(
        message,
        fg='green',
        bold=True
    ))


def init():
    """
    Detects, prompts and initialises the project.
    """
    info('Indexing repository...')
    repository = index_repository()
    click.echo(repository.owner)
    return repository

