import pandas as pd

start_date = "Start date"
start_time = "Start time"
end_date = "End date"
end_time = "End time"
duration = "Duration"

df = pd.read_csv("input/Toggl_time_entries.csv")[[start_date, duration, start_time, end_date, end_time]]

df["start_datetime"] = pd.to_datetime(df[start_date] + "T" + df[start_time] + "Z")
df["end_datetime"] = pd.to_datetime(df[end_date]  + "T" + df[end_time] + "Z")
df["duration_datetime"] = df["end_datetime"] - df["start_datetime"]


current_month_time = df.groupby(by=start_date)["duration_datetime"].sum().reset_index().rename(columns={start_date: 'date'})
current_month_time['seconds'] = current_month_time['duration_datetime'].dt.total_seconds()

current_month_time['hours'] = current_month_time['seconds'] // 3600
current_month_time['minutes'] = (current_month_time['seconds'] % 3600) // 60
current_month_time['seconds'] = current_month_time['seconds'] % 60
current_month_time = current_month_time.astype({'seconds': 'int', 'hours': 'int', 'minutes': 'int'}).astype({'seconds': 'str', 'hours': 'str', 'minutes': 'str'})
current_month_time['duration'] = current_month_time['hours'] + ":" + current_month_time['minutes'] + ":" + current_month_time["seconds"]

current_month = df.loc[0, 'start_datetime'].month
current_year = df.loc[0, 'start_datetime'].year

all_dates_from_current_month = pd.DataFrame({'date':pd.date_range(start=f"{current_year}-{current_month}-01", end=f"{current_year}-{current_month + 1}-01", inclusive="left")}).astype({'date': 'str'})
all_dates_from_current_month = all_dates_from_current_month.merge(current_month_time[['date', 'duration']], on='date', how='left').fillna("00:00:00")

for duration in all_dates_from_current_month['duration']:
    if duration == "00:00:00":
        print("")
    else:
        print(duration)
