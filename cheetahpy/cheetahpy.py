import requests
import io

import pandas as pd

class CheetahPy():
    def __init__(self, api_base="http://localhost:12021"):
        self.api_base = api_base
        import requests
import io

import pandas as pd
    def _test_server(self):
        r = requests.get(self.api_base)
        assert r.status_code == 200, "GC server unavailable"
        return "Server available"
    
    def show_athletes(self):
        try:
            available_athletes = ', '.join(self.athletes) 
        except:
            self._get_athletes()
            available_athletes = ', '.join(self.athletes)
        print(available_athletes)
    
    def _get_athletes(self):
        endpoint = '/'
        r = self._request(endpoint=endpoint)
        self.athletes = []
        for athlete in r.text.split('\n')[1:-1]:
            athlete_name = athlete.split(',')[0]
            self.athletes.append(athlete_name)
            
    def _validate_athlete(self, athlete):
        try:
            available_athletes = ', '.join(self.athletes) 
        except:
            self._get_athletes()
            available_athletes = ', '.join(self.athletes)
        assert athlete in self.athletes, f"Invalid athlete. Choose from:\n {available_athletes}"
        return True
            
    def get_zones(self, athlete, _for='power', sport='Bike'):
        self._validate_athlete(athlete=athlete)
        url_safe_athlete_name =  athlete.replace(' ','%20')
        endpoint = f'/{url_safe_athlete_name}/zones'
        
        params = {'for':_for,
                  'Sport':sport}
        
        r = self._request(endpoint=endpoint, params=params)
        stream = io.StringIO(r.text)
        df = pd.read_csv(stream, sep=",")
        return df
        
        
    def get_activities(self, athlete, start_date, end_date, metrics=None, metadata=None, intervals=False):
        """
        since=yyyy/mm/dd
        before=yyyy/mm/dd
        metrics=NP,IF,TSS,AveragePower
        metadata=none or all or list (Sport,Workout Code)
        intervals=true
        """

        # Check for valid athlete
        self._validate_athlete(athlete)
        
        # Moderate parameters
        url_safe_athlete_name = athlete.replace(' ','%20')
        endpoint = '/' + url_safe_athlete_name
        if type(metrics) == list:
            metrics = ','.join(metrics)
        if type(metadata) == list:
            metadata = ','.join(metadata)

        # Finalize params
        params = {'since':start_date,
                  'before':end_date,
                  'metrics':metrics,
                  'metadata':metadata,
#                   'intervals':intervals
                 }
        # Execute
        r = self._request(endpoint=endpoint, params=params)
        stream = io.StringIO(r.text)
        df = pd.read_csv(stream, sep=",")
        return df
    
    def _request(self, endpoint, params=None, stream=False):
        r = requests.get(self.api_base + endpoint, params=params)
        return r
#     def _build_request(self, endpoint, params=None):
        
#         return 0
#     def _make_request(self, req_string):
#         r = request.get(req_string)
#         return r