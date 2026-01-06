"""
Setup script for the Boilerplate Manager package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from VERSION file
version = (this_directory / "VERSION").read_text(encoding='utf-8').strip()

setup(
    name="boilerplate-manager",
    version=version,
    author="Juan",
    description="A CLI tool for managing and creating projects from boilerplate templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhd3197/boilerplates",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'boilerplates': [
            'templates/**/*',
            'templates/**/**/*',
            'templates/**/**/**/*',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.7",
    install_requires=[
        'InquirerPy>=0.3.4',
    ],
    entry_points={
        'console_scripts': [
            'boilerplates=boilerplates.cli:main',
        ],
    },
)
