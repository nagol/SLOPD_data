import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md

sns.set_theme(style="whitegrid")

# Grab data from repo
pd_data = pd.read_csv("data/csv/SLOPD_report.csv")
pd_data.type = pd_data.type.str.strip()
pd_data['date'] = pd.to_datetime(pd_data['date'], format = '%m/%d/%y')

# Tabulate by call type - i.e. ROBBERY, ASSULT, DUI,...
type_table = (
    pd_data[["type"]]
    .groupby(["type"])
    .size()
    .reset_index()
    .sort_values(by=[0], ascending=[False])
)
type_table.rename(columns={0: "count"}, inplace=True)
type_table.type = type_table.type.str.upper()
type_table = type_table.head(50)
print(type_table)

# Count the calls per day, most recent day may be imcomplete so remove
calls_per_day_table = pd_data[["date"]].groupby("date").size().reset_index()
calls_per_day_table.rename(columns={0: "count"}, inplace=True)
calls_per_day_table.head()

# Initialize the matplotlib figure for barchart ----
f, ax = plt.subplots(figsize=(7, 15))

# Plot frequency of each type of call
sns.set_color_codes("pastel")
sns.barplot(
    x="count",
    y="type",
    data=type_table,
    order=type_table.sort_values("count", ascending=False).type,
    color="b",
    ci=None,
)
ax.set(ylabel="", xlabel="Count")
sns.despine(left=True, bottom=True)


# Save barchart
f.savefig("img/barchart.png", bbox_inches="tight")

# Initialize the matplotlib figure for time-series plot ----
f, ax = plt.subplots(figsize=(15, 7))

sns.lineplot(
    x="date",
    y="count",
    markers=True,
    data=calls_per_day_table[
        calls_per_day_table.date != calls_per_day_table.date.max()
    ],
)
ax.set(ylim=(0, None))

# specify the position of the major ticks at the beginning of the week
ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday = 1))
# specify the format of the labels as 'year-month-day'
ax.xaxis.set_major_formatter(md.DateFormatter('%m/%d/%y'))
# (optional) rotate by 90° the labels in order to improve their spacing
plt.setp(ax.xaxis.get_majorticklabels(), rotation = 90)

# specify the position of the minor ticks at each day
ax.xaxis.set_minor_locator(md.DayLocator(interval = 1))

# set ticks length
ax.tick_params(axis = 'x', which = 'major', length = 10)
ax.tick_params(axis = 'x', which = 'minor', length = 5)

plt.setp(ax.get_xticklabels(), rotation=90)

# Save time-series plot
f.savefig("img/time_series_plot.png", bbox_inches="tight")
