"""Generates a github changelog, tags and uploads your python library"""
from changes.config import Changes, Project
from changes.models.repository import GitHubRepository

__version__ = '0.7.0'
__url__ = 'https://github.com/michaeljoseph/changes'
__author__ = 'Michael Joseph'
__email__ = 'michaeljoseph@gmail.com'


from .cli import main  # noqa

settings = None
project_settings = None


def initialise():
    """
    Detects, prompts and initialises the project.

    Stores project and tool configuration in the `changes` module.
    """
    global settings, project_settings

    # Global changes settings
    settings = Changes.load()

    # Project specific settings
    project_settings = Project.load(
        GitHubRepository(
            auth_token=settings.auth_token
        )
    )
