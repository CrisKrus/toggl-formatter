# go to https://track.toggl.com/profile on the section "API token" you can get yours

import os

import pandas as pd
import requests
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

TOGGL_PROFILE_TOKEN = os.getenv("TOGGL_PROFILE_TOKEN")

workspaces = requests.get(
    'https://api.track.toggl.com/api/v8/workspaces',
    auth=(TOGGL_PROFILE_TOKEN, "api_token"),
)

# from now, we will take just the first workspace_id
first_workspace_id = workspaces.json()[0]["id"]

details = requests.get(
    "https://api.track.toggl.com/reports/api/v2/details/.csv",
    auth=(TOGGL_PROFILE_TOKEN, "api_token"),
    params={
        "workspace_id": first_workspace_id,
        "since": "2022-05-01",
        "until": "2022-06-01",
        "user_agent": "mail@some.domain"
    }
)

# we delete the first 3 characters because are weird ï»¿
# in some point we should investigate why is coming
# if it does not come we are deleting 'Use' from 'User' header
detailed_report = details.text[3:]

df = pd.read_csv(StringIO(detailed_report))

print(df.head())
