
"""
Configuration management for the Boilerplate Manager.
"""

import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".boilerplates"
CONFIG_FILE = CONFIG_DIR / "config.json"
CACHE_DIR = CONFIG_DIR / "cache"

DEFAULT_CONFIG = {
    "github_token": None,
    "private_repos": [],
    "public_repo_url": "https://raw.githubusercontent.com/username/repo/main/public-templates.json"
}

def ensure_config_dir_exists():
    """Ensures that the configuration directory and cache directory exist."""
    CONFIG_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)

def load_config():
    """Loads the configuration from the JSON file."""
    ensure_config_dir_exists()
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # Ensure all default keys are present
            for key, value in DEFAULT_CONFIG.items():
                config.setdefault(key, value)
            return config
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load config file. Using defaults. Error: {e}")
        return DEFAULT_CONFIG

def save_config(config):
    """Saves the configuration to the JSON file."""
    ensure_config_dir_exists()
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Error: Could not save config file. Error: {e}")

