"""MyProject - A robust Python boilerplate with cooperative multiple inheritance.

This package provides a clean, extensible architecture using mixins and
cooperative inheritance patterns.

Main exports:
    - Client: Main application class combining all mixins
    - All individual mixins for custom composition
    - ConfigDict: Configuration dataclass
    - Result: Result type dictionary
"""

import pathlib
import gc
import os
from dotenv import load_dotenv

from .mixins.config import ConfigMixin
from .mixins.tools import ToolsMixin
from .mixins.database import DatabaseMixin
from .mixins.api import APIMixin
from .mixins.logger import LoggerMixin
from .mixins.cache import CacheMixin
from .client import Client
from .types import ConfigDict, Result

# Load environment variables from .env file
load_dotenv()

# Version info
__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = [
    "Client",
    "ConfigMixin",
    "ToolsMixin",
    "DatabaseMixin",
    "APIMixin",
    "LoggerMixin",
    "CacheMixin",
    "ConfigDict",
    "Result",
]
