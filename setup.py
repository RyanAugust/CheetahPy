#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="cheetahpy",
    version="0.4.0",
    author="Ryan Duecker",
    author_email='ryan.duecker@yahoo.com',
    description="Python wrapper for working with the Golden Cheetah API & opendata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas','requests'],
    python_requires='>=3.8',
    url="https://github.com/RyanAugust/CheetahPy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
    ],
    extras_require={
        'linting': [
            "flake8",
            "pylint",
            "mypy",
            "pre-commit",
        ],
        "testing": [
            "pytest"
            ]
    },
    
)