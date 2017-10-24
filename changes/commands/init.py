import changes
from ..config import Project, Changes


def init():
    """
    Detects, prompts and initialises the project.
    """
    # Store config and environment in the changes module

    # Global changes settings
    changes.settings = Changes.load()

    # Project specific settings
    changes.project_settings = Project.load()
