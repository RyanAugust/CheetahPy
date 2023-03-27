import cheetahpy
gc = CheetahPy()

r = gc.get_activities(athlete='Ryan Duecker'
                      ,start_date="2022/01/20"
                      ,end_date="2022/01/30"
                      ,metrics=['Duration','Distance','TSS','NP','IF']
                      ,metadata=['Sport','Workout_Code','Workout_Title','Shoes','Frame','Indoor'])
print('successfully retrieved filtered athlete activities with custom metrics and metadata appended')

r = gc.get_zones(athlete='Ryan Duecker', _for='hr', sport='Run')
print('successfully retrieved athlete hr zones for running')