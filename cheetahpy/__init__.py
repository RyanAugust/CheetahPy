__title__ = 'CheetahPy'
__version__ = '0.3.0'
__author__ = 'RyanAugust'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023'


import io
import requests
import pandas

from .cheetahpy import CheetahPy_API

CheetahPy = CheetahPy_API()

__all__ = [
    'CheetahPy',
]
