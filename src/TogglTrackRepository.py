import os

import pandas as pd
import requests
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

TOGGL_PROFILE_TOKEN = os.getenv("TOGGL_PROFILE_TOKEN")


class TogglTrackRepository:
    API_TOKEN = USER_AGENT = None

    def __init__(self, token: str, user_agent: str):
        self.API_TOKEN = token
        self.USER_AGENT = user_agent

    def get_report_detailed(self, workspace: str, date_since: str, date_until: str):
        report_details = requests.get(
            "https://api.track.toggl.com/reports/api/v2/details/.csv",
            auth=(self.API_TOKEN, "api_token"),
            params={
                "workspace_id": workspace,
                "since": date_since,
                "until": date_until,
                "user_agent": self.USER_AGENT
            }
        ).text

        # we delete the first 3 characters because are weird ï»¿
        # in some point we should investigate why is coming
        # if it does not come we are deleting 'Use' from 'User' header
        if report_details.startswith("User", beg=0, end=8):
            return report_details

        return report_details[3:]

    def get_workspaces(self):
        workspaces = requests.get(
            'https://api.track.toggl.com/api/v8/workspaces',
            auth=(self.API_TOKEN, "api_token"),
        )

        return workspaces.json

# from now, we will take just the first workspace_id
first_workspace_id = workspaces.json()[0]["id"]

df = pd.read_csv(StringIO(detailed_report))

print(df.head())
