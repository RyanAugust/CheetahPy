"""Module providing python wrapper to Golden Cheetah data"""
__title__ = 'CheetahPy'
__version__ = '0.4.0'
__author__ = 'RyanAugust'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023'


# import requests
# import pandas

from .cheetahpy import CheetahPy_API
from .local_opendata import opendata_dataset

CheetahPy = CheetahPy_API()

__all__ = [
    'CheetahPy',
    'opendata_dataset'
]
