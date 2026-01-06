"""
Boilerplate Manager - A CLI tool for managing project templates.
"""
import importlib.metadata

try:
    __version__ = importlib.metadata.version("boilerplate-manager")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

__author__ = "Juan"
