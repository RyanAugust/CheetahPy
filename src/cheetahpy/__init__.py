"""Module providing python wrapper to Golden Cheetah data"""
__title__ = 'CheetahPy'
__author__ = 'RyanAugust'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023'

import os
with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

from .cheetahpy import CheetahPy_API
from .local_opendata import opendata_dataset

__all__ = [
    'CheetahPy',
    'opendata_dataset'
]
