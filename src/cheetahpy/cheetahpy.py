"""Module providing python wrapper to the Golden Cheetah API"""
import requests
import pandas as pd
import io


class URLs:
    """Class for retrieving GC AIP URL paths"""
    def __init__(self):
        self._base_url = "http://localhost:12021"

        # athletesurls
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
        return self._base_url

    def athletes_url(self) -> str:
        return self._base_url + self.athletes

    def athlete_url(self) -> str:
        return self._base_url + self.athlete

    def measure_groups_url(self) -> str:
        return self._base_url + self.measures_groups

    def measures_url(self) -> str:
        return self._base_url + self.measures

    def zones_url(self) -> str:
        return self._base_url + self.zones

    def season_meanmax_url(self) -> str:
        return self._base_url + self.season_meanmax

    def activity_meanmax_url(self) -> str:
        return self._base_url + self.activity_meanmax

    def activity_url(self) -> str:
        return self._base_url + self.activity


class CheetahPy_API:
    def __init__(self, test_server: bool = False):
        self.urls = URLs()
        if test_server:
            print(self._test_server())

    def _test_server(self):
        try:
            r = requests.get(self.urls.base_url())
            status_ = "API unavailable. Start GC and ensure API is enabled" if r.status_code != 200 else "API available"
        except Exception as err:
            status_ = f"{err}: API unavailable. Start GC and ensure API is enabled"
        return status_

    def show_athletes(self):
        try:
            available_athletes = ', '.join(self.athletes)
        except Exception as err:
            print(f"{err}: Athletes undefinded, referencing API to load athletes")
            self._get_athletes()
            available_athletes = ', '.join(self.athletes)
        print(available_athletes)

    def _get_data(self, url:str, params=None):
        """Wrapper function for the requests.get function"""
        r = requests.get(url, params=params)
        return r

    def _get_athletes(self):
        """Helper function that returns all available athletes from the connected
        GC instance"""
        url = self.urls.athletes_url()
        r = self._get_data(url)

        self.athletes = []
        for athlete in r.text.split('\n')[1:-1]:
            athlete_name = athlete.split(',')[0]
            self.athletes.append(athlete_name)

    def _validate_athlete(self, athlete:str) -> bool:
        """Helper function that ensures that a passed athlete is actually available
        within the connected GC instance."""
        try:
            available_athletes = ', '.join(self.athletes)
        except Exception as err:
            print(f"{err}: Athletes undefinded, referencing API to load athletes")
            self._get_athletes()
            available_athletes = ', '.join(self.athletes)
        assert athlete in self.athletes, f"Invalid athlete. Choose from:\n {available_athletes}"
        return True

    def _url_safe_athlete_name(self, athlete_name:str) -> str:
        """Helper function ensuring that passed athlete name is format safe to
        be passed to the API"""
        url_safe_athlete_name = athlete_name.replace(' ','%20')
        return url_safe_athlete_name

    @staticmethod
    def _csv_text_to_df(csv_text:str, sep=",") -> pd.DataFrame:
        """Helper function to convert text returned by the AIP in a CSV format
        into a pandas dataframe object"""
        stream = io.StringIO(csv_text)
        df = pd.read_csv(stream, sep=sep)
        df.rename(mapper=lambda col_name: col_name.strip(' "'), axis=1, inplace=True)
        # df.columns = [{col:col.strip(' "')} for col in df.columns.tolist()]
        return df

    def get_athlete_summary(self, athlete:str) -> pd.DataFrame:
        """Retrieves activity summary (ie activity grain) metrics and metadata
        for a given athlete"""
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)

        url = self.urls.athlete_url()
        r = self._get_data(url.format(athlete_name=url_safe_athlete_name))
        df = self._csv_text_to_df(r.text)
        return df

    def get_measure_groups(self, athlete:str) -> list:
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)

        url = self.urls.measure_groups_url()
        r = self._get_data(url.format(athlete_name=url_safe_athlete_name))
        measure_groups = r.text.split('\n')
        return measure_groups

    def get_measures(self, athlete:str, measure_group:list, start_date:str, end_date:str) -> pd.DataFrame:
        """
        measure_group must be valid and can be looked up using `get_measure_groups`
        start_date=yyyy/mm/dd
        end_date=yyyy/mm/dd
        """
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        params = {'since':start_date,
                  'before':end_date}

        url = self.urls.measures_url()
        r = self._get_data(
            url.format(athlete_name=url_safe_athlete_name,
                       measure_group=measure_group),
            params)
        df = self._csv_text_to_df(r.text)
        return df

    def get_zones(self, athlete:str, _for:str = 'power', sport:str = 'Bike') -> pd.DataFrame:
        """Return dataframe with zone specifications for a designated athelte,
        sport, and type of measurement"""
        self._validate_athlete(athlete=athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        url = self.urls.zones_url()

        params = {'for': _for,
                  'Sport': sport}

        r = self._get_data(url.format(athlete_name=url_safe_athlete_name),
                           params=params)
        df = self._csv_text_to_df(r.text)
        return df

    def get_meanmax(
        self,
        athlete:str,
        series:str,
        activity_filename = None,
        start_date = None,
        end_date = None) -> pd.DataFrame:
        """
        Retrieves meanmax based on either a single activity OR a daterange
        Series :: designates the meanmax series that is returned via csv
            options: []
        """
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)

        if activity_filename is not None and (start_date is None and end_date is None):
            url = self.urls.activity_meanmax_url()
            params = {'series':series}
            r = self._get_data(
                url.format(athlete_name=url_safe_athlete_name,
                    activity_filename=activity_filename),
                params=params)

        elif (start_date is not None and end_date is not None) and activity_filename is None:
            url = self.urls.season_meanmax_url()
            params = {'series': series,
                      'since': start_date,
                      'before': end_date}
            r = self._get_data(url.format(athlete_name=url_safe_athlete_name), params=params)

        else:
            assert "Must designate either an activity filename OR a start & end date"

        df = self._csv_text_to_df(r.text)
        return df

    def get_activities(
            self,
            athlete:str,
            start_date:str,
            end_date:str,
            metrics = None,
            metadata = None,
            intervals:bool = False,
            activity_filenames_only:bool = False):
        """since=yyyy/mm/dd
        before=yyyy/mm/dd
        metrics=NP,IF,TSS,AveragePower
        metadata=none or all or list (Sport,Workout Code)
        intervals=true"""
        # Check for valid athlete
        self._validate_athlete(athlete)

        # Ensure minimum return for filenames only
        if activity_filenames_only:
            metadata = None
            metrics = None

        # Moderate parameters
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        url = self.urls.athlete_url()

        if isinstance(metrics, list):
            metrics = ','.join(metrics)
        if isinstance(metadata, list):
            metadata = ','.join(metadata)

        # Finalize params
        params = {'since': start_date,
                  'before': end_date,
                  'metrics': metrics,
                  'metadata': metadata,
                  'intervals': intervals
                  }
        # Execute
        r = self._get_data(
            url.format(athlete_name=url_safe_athlete_name),
            params=params)
        df = self._csv_text_to_df(r.text)

        if activity_filenames_only:
            filenames = df['filename'].tolist()
            return filenames
        else:
            return df

    def get_activity(self, athlete:str, activity_filename:str, _format:str = 'csv'):
        """
        Returns the activity data for a given athlete + activity filename.
        You may specify the format to be returned, which can be: csv, tcx, json, pwx
        Using a format of csv will return a pandas dataframe object
            otherwise a raw requests response will be returned.
        """

        # Check for valid athlete
        self._validate_athlete(athlete)
        url_safe_athlete_name = self._url_safe_athlete_name(athlete_name=athlete)
        url = self.urls.activity_url()

        params = {'format':_format}

        r = self._get_data(
            url.format(
                athlete_name=url_safe_athlete_name,
                activity_filename=activity_filename
                ),
            params=params)
        if _format == 'csv':
            df = self._csv_text_to_df(r.text)
            return df
        else:
            return r
