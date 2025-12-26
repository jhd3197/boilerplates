"""
Setup script for the Boilerplate Manager package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from __init__.py
version = {}
with open(this_directory / "boilerplates" / "__init__.py", encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, version)
            break

setup(
    name="boilerplate-manager",
    version=version.get('__version__', '0.1.0'),
    author="Juan",
    description="A CLI tool for managing and creating projects from boilerplate templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/boilerplates",
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
