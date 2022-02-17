__title__ = 'CheetahPy'
__version__ = '1.0.0'
__author__ = 'RyanAugust'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022'


import io
import requests
import pandas


try:
    from .cheetahpy import CheetahPy
except:
    pass


__all__ = [
    'CheetahPy',
]