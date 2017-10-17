import os
import click
import changes
from ..models import GitRepository
from . import info, note
from ..config import load_settings, load_project_settings


def init():
    """
    Detects, prompts and initialises the project.
    """
    # Store config and environment in the changes module

    # Global changes settings
    changes.settings = load_settings()

    # Project specific settings
    changes.project_settings = load_project_settings()


    return changes.project_settings.repository

