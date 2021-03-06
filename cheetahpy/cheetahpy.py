import requests
import io
import pandas

class URLs(object):
    def __init__(self):
        self.base_url = "http://localhost:12021"

        # athletes
        self.athletes = "/"
        self.athlete = "/{athlete_name}"

        # measures
        self.measures_groups = "/{athlete_name}/measures"
        self.measures = "/{athlete_name}/measures/{measure_group}"

        # zones
        self.zones = "/{athlete_name}/zones"

        # seasons
        self.season_meanmax = "/{athlete_name}/meanmax/bests"

        # activities
        self.activity = "/{athlete_name}/activity/{activity_filename}"
        self.activity_meanmax = "/{athlete_name}/meanmax/{activity_filename}"

    def base_url(self):
        return self.base_url

    def athletes_url(self):
        return self.base_url + self.athletes

    def athlete_url(self):
        return self.base_url + self.athlete

    def measure_groups_url(self):
        return self.base_url + self.measures_groups

    def measures_url(self):
        return self.base_url + self.measures

    def zones_url(self):
        return self.base_url + self.zones

    def season_meanmax_url(self):
        return self.base_url + self.season_meanmax

    def activity_meanmax_url(self):
        return self.base_url + self.activity_meanmax

    def activity_url(self):
        return self.base_url + self.activity

class CheetahPy(object):
    def __init__(self):
        self.url = URLs()
        
    def _test_server(self):
        r = requests.get(self.url.base_url)
        assert r.status_code == 200, "GC server unavailable"
        return "Server available"
    
    def show_athletes(self):
        try:
            available_athletes = ', '.join(self.athletes) 
        except:
            self._get_athletes()
            available_athletes = ', '.join(self.athletes)
        print(available_athletes)

    def _get_data(self, url, params=None):
        r = requests.get(url, params=params)
        return r
    
    def _get_athletes(self):
        url = self.url.athletes_url()
        r = self._get_data(url)

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
    
    def _url_safe_athlete_name(self, athlete_name):
        url_safe_athlete_name = athlete_name.replace(' ','%20')
        return url_safe_athlete_name
    
    @staticmethod
    def _csv_text_to_df(csv_text, sep=","):
        stream = io.StringIO(csv_text)
        df = pandas.read_csv(stream, sep=sep)
        return df

    def get_athlete_details(self, athlete):
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        
        url = self.url.athlete_url()
        r = self._get_data(url.format(athlete_name=url_safe_athlete_name))
        df = self._csv_text_to_df(r.text)
        return df

    def get_measure_groups(self, athlete):
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        
        url = self.url.measure_groups_url()
        r = self._get_data(url.format(athlete_name=url_safe_athlete_name))
        measure_groups = r.text.split('\n')
        return measure_groups
    
    def get_measures(self, athlete, measure_group, start_date, end_date):
        """
        measure_group must be valid and can be looked up using `get_measure_groups`
        start_date=yyyy/mm/dd
        end_date=yyyy/mm/dd
        """
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        params = {'since':start_date,
                  'before':end_date}

        url = self.url.measures_url()
        r = self._get_data(url.format(athlete_name=url_safe_athlete_name
                                     ,measure_group=measure_group)
                           ,params)
        df = self._csv_text_to_df(r.text)
        return df
            
    def get_zones(self, athlete, _for='power', sport='Bike'):
        self._validate_athlete(athlete=athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        url = url.zones_url()
        
        params = {'for':_for,
                  'Sport':sport}
        
        r = self._get_data(url.format(athlete_name=url_safe_athlete_name)
                          , params=params)
        df = self._csv_text_to_df(r.text)
        return df
        
    def get_meanmax(self
                    ,athlete
                    ,series
                    ,activity_filename=None
                    ,start_date=None
                    ,end_date=None):
        """
        Retrieves meanmax based on either a single activity OR a daterange
        Series :: designates the meanmax series that is returned via csv
            options: []
        """
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)

        if activity_filename!=None and (start_date==None and end_date==None):
            url = self.url.activity_meanmax_url()
            params = {'series':series}
            r = self._get_data(url.format(athlete_name=url_safe_athlete_name
                                         ,activity_filename=activity_filename)
                              , params=params)

        elif (start_date!=None and end_date!=None) and activity_filename==None:
            url = self.url.season_meanmax_url()
            params = {'series':series
                      ,'since':start_date
                      ,'before':end_date}
            r = self._get_data(url.format(athlete_name=url_safe_athlete_name), params=params)

        else:
            assert "Must designate either an activity filename OR a start & end date"

        df = self._csv_text_to_df(r.text)
        return df

    def get_activities(self
                       ,athlete
                       ,start_date
                       ,end_date
                       ,metrics=None
                       ,metadata=None
                       ,intervals=False
                       ,activity_filenames_only=False):
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
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        url = self.url.athlete_url()

        if type(metrics) == list:
            metrics = ','.join(metrics)
        if type(metadata) == list:
            metadata = ','.join(metadata)

        # Finalize params
        params = {'since':start_date,
                  'before':end_date,
                  'metrics':metrics,
                  'metadata':metadata,
                  'intervals':intervals
                 }
        # Execute
        r = self._get_data(url.format(athlete_name=url_safe_athlete_name)
                                     , params=params)
        df = self._csv_text_to_df(r.text)
        return df
    
    def get_activity(self, athlete, activity_filename, _format='csv'):
        """
        Returns the activity data for a given athlete + activity filename.
        You may specify the format to be returned, which can be: csv, tcx, json, pwx
        Using a format of csv will return a pandas dataframe object 
            otherwise a raw requests response will be returned.
        """
        
        # Check for valid athlete
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        url = self.url.activity_url()
        
        params = {'format':_format}
        
        r = self._get_data(self.url.format(athlete_name=url_safe_athlete_name
                                          ,activity_filename=activity_filename)
                          , params=params)
        if _format == 'csv':
            df = self._csv_text_to_df(r.text)
            return df
        else:
            return r

