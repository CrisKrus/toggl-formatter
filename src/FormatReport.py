import pandas as pd

start_date = "Start date"
start_time = "Start time"
end_date = "End date"
end_time = "End time"
duration = "Duration"


class FormatReport:
    @staticmethod
    def _calculate_date_time(df: pd.DataFrame) -> pd.DataFrame:
        df["start_datetime"] = pd.to_datetime(df[start_date] + "T" + df[start_time] + "Z")
        df["end_datetime"] = pd.to_datetime(df[end_date] + "T" + df[end_time] + "Z")
        df["duration_datetime"] = df["end_datetime"] - df["start_datetime"]

        return df

    @staticmethod
    def _calculate_working_hours_per_date(df: pd.DataFrame) -> pd.DataFrame:
        current_month_time = df.groupby(by=start_date)["duration_datetime"].sum().reset_index().rename(
            columns={start_date: 'date'})
        current_month_time['seconds'] = current_month_time['duration_datetime'].dt.total_seconds()

        current_month_time['hours'] = current_month_time['seconds'] // 3600
        current_month_time['minutes'] = (current_month_time['seconds'] % 3600) // 60
        current_month_time['seconds'] = current_month_time['seconds'] % 60
        current_month_time = current_month_time\
            .astype({'seconds': 'int', 'hours': 'int', 'minutes': 'int'})\
            .astype({'seconds': 'str', 'hours': 'str', 'minutes': 'str'})
        current_month_time['duration'] = f"{current_month_time['hours']}:{current_month_time['minutes']}:{current_month_time['seconds']}"

        return current_month_time[['date', 'duration']]

    @staticmethod
    def _get_current_month(df: pd.DataFrame) -> str:
        return df.loc[0, 'start_datetime'].month

    @staticmethod
    def _get_current_year(df: pd.DataFrame) -> str:
        return df.loc[0, 'start_datetime'].year

    @staticmethod
    def _calculate_all_dates_from_month(month: str, year: str) -> pd.DataFrame:
        return pd.DataFrame({
            'date': pd.date_range(
                start=f"{year}-{month}-01",
                end=f"{year}-{int(month) + 1}-01",
                inclusive="left")
        }).astype({'date': 'str'})

    @staticmethod
    def _fill_all_month_dates_with_working_hours(month_dates: pd.DataFrame,
                                                 working_hours: pd.DataFrame) -> pd.DataFrame:
        return month_dates.merge(working_hours, on='date', how='left').fillna("00:00:00")

    def get_monthly_report(self, df):
        df = self._calculate_date_time(df)
        working_hours = self._calculate_working_hours_per_date(df)

        current_year = self._get_current_year(df)
        current_month = self._get_current_month(df)

        all_dates_from_current_month = self._calculate_all_dates_from_month(current_month, current_year)

        working_hours_per_date = self._fill_all_month_dates_with_working_hours(all_dates_from_current_month,
                                                                               working_hours)

        return working_hours_per_date
