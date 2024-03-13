# import pytest

import cheetahpy

# r = CheetahPy.get_activities(athlete='Ryan Duecker'
#                       ,start_date="2022/01/20"
#                       ,end_date="2022/01/30"
#                       ,metrics=['Duration','Distance','TSS','NP','IF']
#                       ,metadata=['Sport','Workout_Code','Workout_Title','Shoes','Frame','Indoor'])
# print('successfully retrieved filtered athlete activities with custom metrics and metadata appended')

# r = CheetahPy.get_zones(athlete='Ryan Duecker', _for='hr', sport='Run')
# print('successfully retrieved athlete hr zones for running')

def test_base_url():
    CP_AIP = cheetahpy.CheetahPy_API()
    result = CP_AIP.urls.base_url()
    assert result == "http://localhost:12021"

if __name__ == '__main__':
    test_base_url()

    print("Everything passed")
