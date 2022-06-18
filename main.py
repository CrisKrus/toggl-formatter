import os
from io import StringIO

import pandas as pd
from dotenv import load_dotenv

from src.formatReport import FormatReport
from src.togglTrackRepository import TogglTrackRepository

load_dotenv()

TOGGL_PROFILE_TOKEN = os.getenv("TOGGL_PROFILE_TOKEN")
USER_AGENT = os.getenv("USER_AGENT")

start_date = "Start date"
start_time = "Start time"
end_date = "End date"
end_time = "End time"
duration = "Duration"

toggl_repository = TogglTrackRepository(TOGGL_PROFILE_TOKEN, USER_AGENT)
workspaces = toggl_repository.get_workspaces()

# from now, we will take just the first workspace_id
first_workspace_id = workspaces[0]["id"]

detailed_report = toggl_repository.get_report_detailed(first_workspace_id, "2022-05-01", "2022-06-01")

df = pd.read_csv(StringIO(detailed_report))

# df = pd.read_csv("input/Toggl_time_entries.csv")[[start_date, duration, start_time, end_date, end_time]]

reporter = FormatReport()
monthly_report = reporter.get_monthly_report(df)

for duration in monthly_report['duration']:
    if duration == "00:00:00":
        print("")
    else:
        print(duration)

