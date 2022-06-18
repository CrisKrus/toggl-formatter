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
                "start_datetime": "2022-02-02T20:20:20Z",
                "end_datetime": "2022-02-02T22:20:20Z",
                "duration_datetime": pd.Timedelta("2 hours"),
            },
            {
                "Start date": "2022-02-02",
                "start_datetime": "2022-02-02T20:20:20Z",
                "end_datetime": "2022-02-02T22:20:20Z",
                "duration_datetime": pd.Timedelta("2 hours"),
            },
            {
                "Start date": "2022-02-03",
                "start_datetime": "2022-02-03T20:20:20Z",
                "end_datetime": "2022-02-03T22:20:20Z",
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


if __name__ == '__main__':
    unittest.main()
