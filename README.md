# Toggl formatter

## How to get data to work with

Download the month that you want to process. It should be the detailed report. Something like:

```
https://track.toggl.com/reports/detailed/1998184/clients/56277049/period/thisMonth
```

## How to run

1. `pipenv shell`
2. `pipenv install`
3. Fill input file with data `input/Toggl_time_entries.csv`
4. `python main.py`
