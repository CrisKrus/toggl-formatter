import unittest

import pandas as pd
from pandas._testing import assert_frame_equal

from src.formatReport import FormatReport


class TestFormatReport(unittest.TestCase):
    def test_calculate_date_time(self):
        df = pd.DataFrame([
            {
                "Start date": "2022-02-02",
                "Start time": "20:20:20",
                "End date": "2022-02-02",
                "End time": "22:20:20",
            }
        ])

        result = FormatReport._calculate_date_time(df)

        expected = pd.DataFrame([
            {
                "Start date": "2022-02-02",
                "Start time": "20:20:20",
                "End date": "2022-02-02",
                "End time": "22:20:20",
                "start_datetime": "2022-02-02T20:20:20Z",
                "end_datetime": "2022-02-02T22:20:20Z",
                "duration_datetime": pd.Timedelta("2 hours"),
            }
        ]).astype({"start_datetime": "datetime64", "end_datetime": "datetime64"})

        assert_frame_equal(result, expected, check_dtype=False)

    def test_calculate_working_hours_per_date(self):
        df = pd.DataFrame([
            {
                "Start date": "2022-02-02",
                "duration_datetime": pd.Timedelta("2 hours"),
            },
            {
                "Start date": "2022-02-02",
                "duration_datetime": pd.Timedelta("2 hours"),
            },
            {
                "Start date": "2022-02-03",
                "duration_datetime": pd.Timedelta("2 hours"),
            },
        ])

        result = FormatReport._calculate_working_hours_per_date(df)

        expected = pd.DataFrame([
            {
                "date": "2022-02-02",
                "duration": "4:0:0",
            },
            {
                "date": "2022-02-03",
                "duration": "2:0:0",
            },
        ])

        assert_frame_equal(result, expected)

    def test_calculate_all_dates_for_month(self):
        month = "02"
        year = "2022"

        result = FormatReport._calculate_all_dates_from_month(month, year)

        expected = pd.DataFrame([
            "2022-02-01", "2022-02-02", "2022-02-03", "2022-02-04", "2022-02-05", "2022-02-06", "2022-02-07",
            "2022-02-08", "2022-02-09", "2022-02-10", "2022-02-11", "2022-02-12", "2022-02-13", "2022-02-14",
            "2022-02-15", "2022-02-16", "2022-02-17", "2022-02-18", "2022-02-19", "2022-02-20", "2022-02-21",
            "2022-02-22", "2022-02-23", "2022-02-24", "2022-02-25", "2022-02-26", "2022-02-27", "2022-02-28",
        ], columns=["date"])

        assert_frame_equal(result, expected)

    def test_fill_all_month_dates_with_working_hours(self):
        month_dates = pd.DataFrame(["2022-02-01", "2022-02-02", "2022-02-03"], columns=["date"])
        working_hours = pd.DataFrame([
            {
                "date": "2022-02-01",
                "duration": "4:0:0",
            },
            {
                "date": "2022-02-02",
                "duration": "4:0:0",
            },
            {
                "date": "2022-02-03",
                "duration": "2:0:0",
            },
        ])

        result = FormatReport._fill_all_month_dates_with_working_hours(month_dates, working_hours)

        expected = pd.DataFrame([
            {
                "date": "2022-02-01",
                "duration": "4:0:0",
            },
            {
                "date": "2022-02-02",
                "duration": "4:0:0",
            },
            {
                "date": "2022-02-03",
                "duration": "2:0:0",
            },
        ])
        assert_frame_equal(result, expected)

    def test_fill_all_month_dates_with_working_hours_complete_empty_days_with_0_hours(self):
        day_with_missing_working_hours = "2022-02-02"
        month_dates = pd.DataFrame(["2022-02-01", day_with_missing_working_hours, "2022-02-03"], columns=["date"])
        working_hours = pd.DataFrame([
            {
                "date": "2022-02-01",
                "duration": "4:0:0",
            },
            {
                "date": "2022-02-03",
                "duration": "2:0:0",
            },
        ])

        result = FormatReport._fill_all_month_dates_with_working_hours(month_dates, working_hours)

        expected = pd.DataFrame([
            {
                "date": "2022-02-01",
                "duration": "4:0:0",
            },
            {
                "date": day_with_missing_working_hours,
                "duration": "00:00:00",
            },
            {
                "date": "2022-02-03",
                "duration": "2:0:0",
            },
        ])
        assert_frame_equal(result, expected)

    def test_fill_all_month_dates_with_working_hours_not_fill_working_hours_outside_of_the_month(self):
        month_dates = pd.DataFrame(["2022-02-01", "2022-02-02"], columns=["date"])
        date_outside_of_the_month = "2022-02-03"
        working_hours = pd.DataFrame([
            {
                "date": "2022-02-01",
                "duration": "4:0:0",
            },
            {
                "date": "2022-02-02",
                "duration": "4:0:0",
            },
            {
                "date": date_outside_of_the_month,
                "duration": "2:0:0",
            },
        ])

        result = FormatReport._fill_all_month_dates_with_working_hours(month_dates, working_hours)

        expected = pd.DataFrame([
            {
                "date": "2022-02-01",
                "duration": "4:0:0",
            },
            {
                "date": "2022-02-02",
                "duration": "4:0:0",
            },
        ])
        assert_frame_equal(result, expected)

if __name__ == '__main__':
    unittest.main()
