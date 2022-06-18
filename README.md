# Toggl formatter

## How to get data to work with

Download the month that you want to process. It should be the detailed report. Something like:

```
https://track.toggl.com/reports/detailed/1998184/clients/56277049/period/thisMonth
```

## Set up

You will need to create a file in the root directory: `.env` in order to get data from toggl API.
This file should be like the following:

```text
TOGGL_PROFILE_TOKEN={your_token_here}
```

### Where can I find my toggl track token?

Go to <https://track.toggl.com/profile> scroll to the bottom and look for the section "API token" to get yours.

## How to run

1. `pipenv shell`
2. `pipenv install`
3. Fill input file with data `input/Toggl_time_entries.csv`
4. `python main.py`
