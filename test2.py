import cheetahpy

gc = cheetahpy.CheetahPy()

r = gc.get_activities(athlete='Ryan Duecker'
                      ,start_date="2021/03/01"
                      ,end_date="2022/03/30"
                      ,metrics=['Duration','Distance','TSS','NP','IF','Session_RPE','Time_Moving']
                      ,metadata=['Sport','Workout_Code','Workout_Title','Shoes','Frame','Indoor'])

r.to_csv('./activities.csv')
print('successfully retrieved activitys with metrics, metadata, and date filtering')
