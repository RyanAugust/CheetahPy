# CheetahPy
[![CodeFactor](https://www.codefactor.io/repository/github/ryanaugust/cheetahpy/badge)](https://www.codefactor.io/repository/github/ryanaugust/cheetahpy)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cheetahpy.svg?label=PyPI%20downloads)](
https://pypi.org/project/cheetahpy/)

This module is used to access [Golden Cheetah](https://github.com/GoldenCheetah/GoldenCheetah) based data.
**CheetahPy_API** enables pythonic access to the GC API, allowing for programmatic access to GC rendered data.
**opendata_dataset** enables similar access and summary/activity functions for locally stored opendata project files that have been pre-compiled by GC.

------
Documentation specifically for the API can be found [here](https://github.com/GoldenCheetah/GoldenCheetah/wiki/UG_Special-Topics_REST-API-documentation). However, the basic hierarchy can be referenced below and knowledge of the API is unnecessary for using this module. Broadly the API provides no compute functionality and instead is purely desgined as a raw data retrieval pipeline.

Golden Cheetah has five key object classes: Athletes, Activities, Zones, Measures, and Meanmax.
Athlete is the node from which all others are referenced.
