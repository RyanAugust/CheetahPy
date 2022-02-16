gc = CheetahPy()

r = gc.get_activities(athlete='Ryan Duecker'
                      ,start_date="2022/01/20"
                      ,end_date="2022/01/30"
                      ,metrics=['Duration','Distance','TSS','NP','IF']
                      ,metadata=['Sport','Workout_Code','Workout_Title','Shoes','Frame','Indoor'])

r = gc.get_zones(athlete='Ryan Duecker', _for='hr', sport='Run')
print(r)
