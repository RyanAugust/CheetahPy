# CheetahPy
This module is used to access the locally hosted API provided by within [Golden Cheetah](https://github.com/GoldenCheetah/GoldenCheetah).

Documentation specifically for the API can be found [here](https://github.com/GoldenCheetah/GoldenCheetah/wiki/UG_Special-Topics_REST-API-documentation). However, the basic hierarchy can be referenced below and knowledge of the API is unnecessary for using this module. Broadly the API provides no compute functionality and instead is purely desgined as a raw data retrieval pipeline.

Golden Cheetah has five key object classes: Athletes, Activities, Zones, Measures, and Meanmax.
Athlete is the node from which all others are referenced.
