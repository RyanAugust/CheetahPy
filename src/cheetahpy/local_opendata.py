"""Module providing python wrapper to the Golden Cheetah API"""

import os
import json
import pandas as pd


class opendata_dataset(object):
    def __init__(self, root_dir:str):
        self.root_dir = root_dir
        self.athlete_ids = self.get_athlete_ids()

    def get_athlete_ids(self) -> list:
        """Preform a walk of the local dir for all available athlete IDs.

        Args:
            None
        Returns:
            athletes (list): List of athlete IDs, which equate to the directory their data is stored in."""
        for _,b,_ in os.walk(self.root_dir):
            athletes = b
            athletes.remove('INDEX') if 'INDEX' in athletes else 0
            break
        return athletes

    def show_athlete_ids(self):
        """Display IDs of athletes that are available locally"""
        athlete_id_count = len(self.athlete_ids)
        athlete_ids_joined = ",\n".join(self.athlete_ids)
        ath_id_str = f"AVAILABLE ATHLETE IDS ({athlete_id_count}): \n {athlete_ids_joined}"
        print(ath_id_str)

    def get_list_columns(self, dataframe: pd.DataFrame) -> list:
        list_cols = []
        [list_cols.append(col) if isinstance(dataframe[col].dropna().values[0], list) else None for col in dataframe.columns.tolist()]
        return list_cols

    def get_athlete_summary(self, athlete_id:str, make_float:bool = True) -> pd.DataFrame:
        """Give the activity summary for a given athelte ID.

        Args:
            athlete_id (str): ID string corresponding to an athlete within the opendata directory
            make_float (bool): Attempt to convert all of the metric columns to floats and when encountering a nested list, extract the list into columns
        Returns:
            df (DataFrame): processed summary dataframe, with rows corresponding to activities"""
        ath_summary_path = self._athlete_summary_path(athlete_id=athlete_id)
        with open(ath_summary_path, 'r') as f:
            summary_json = f.read()
            f.close()
        rides = json.loads(summary_json)['RIDES']
        df = pd.json_normalize(rides)
        if make_float:
            metric_cols = []
            [metric_cols.append(col) if 'METRIC' in col else None for col in df.columns.tolist()]
            for col in metric_cols:
                if isinstance(df[col].dropna().values[0], str):
                    df[col] = self._safe_convert(original_series=df[col], type_convert=float)
                else:
                    None

        return df

    def unpack_list_columns(self, dataframe: pd.DataFrame, list_columns: list) -> pd.DataFrame:
        for list_col in list_columns:
            decompression = self._safe_list_decompression(original_series=dataframe[list_col])
            dataframe = dataframe.join(decompression)
            del dataframe[list_col]
        return dataframe

    def get_athlete_activity_files(self, athlete_id:str) -> list:
        """Returns the discrete files representing individual activities for a given athlete ID. These files are direct children of the athlete's directory.

        Args:
            athelte_id (str): ID string corresponding to an athlete within the opendata directory
        Returns:
            activity_files (list): list of file names representing activities that are stored within the athlete directory"""
        athlete_dir = self._athlete_dir(athlete_id=athlete_id)
        for a, b, c in os.walk(athlete_dir):
            raw_files = c
        activity_files = [file for file in raw_files if '.csv' in file]
        return activity_files

    def _athlete_dir(self, athlete_id: str) -> str:
        athlete_dir = os.path.join(self.root_dir, athlete_id)
        return athlete_dir

    def _athlete_summary_path(self, athlete_id: str) -> str:
        summary_filename = "{" + athlete_id + "}.json"
        ath_summary_path = os.path.join(self.root_dir, athlete_id, summary_filename)
        return ath_summary_path

    @staticmethod
    def _safe_convert(original_series:pd.Series, type_convert:type) -> pd.Series:
        try:
            new_series = original_series.astype(type_convert)
            return new_series
        except Exception as err:
            print(f'{err}: cannot convert {type(original_series)} to type {type_convert}')
            return original_series

    @staticmethod
    def _safe_list_decompression(original_series: pd.Series) -> pd.DataFrame:
        """
        Takes a column of lists (col_name) from a dataframe (df)

        Returns a dataframe with number of columns equal to max list size
        and each element of the row list in its own column with column names appending a prefix based on list index
        Args:
            original_series (pd.Series): pandas series that contains lists of data in it's rows
        Returns:
            new_df (pd.DataFrame): dataframe based on the expanded lists of the data contained in original_series.
        """
        col_prefix = original_series.name
        new_df = original_series.apply(pd.Series)
        new_df = new_df.rename(columns = lambda x : col_prefix + '_' + str(x))
        return new_df
