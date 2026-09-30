"""
Root settings module redirecting to config.settings.
Ensures consistency regardless of whether settings or config.settings is imported.
"""
from config.settings import *  # noqa: F401, F403
