
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

# Grab data from repo
pd_data = pd.read_csv("data/csv/SLOPD_report.csv")

# Tabulate by call type - i.e. ROBBERY, ASSULT, DUI,...
type_table = pd_data[['type']].groupby(['type']).size().reset_index().sort_values(by = [0], ascending=[False])
type_table.rename(columns = {0:'count'}, inplace=True)
type_table.type = type_table.type.str.upper()

# Count the calls per day, most recent day may be imcomplete so remove
calls_per_day_table = pd_data[['date']].groupby('date').size().reset_index()
calls_per_day_table.rename(columns = {0: 'count'}, inplace = True)
calls_per_day_table.head()

# Initialize the matplotlib figure for barchart ----
f, ax = plt.subplots(figsize=(7, 15))

# Plot frequency of each type of call
sns.set_color_codes("pastel")
sns.barplot(
    x="count", 
    y="type", 
    data = type_table,
    order = type_table.sort_values('count', ascending=False).type,
    color="b",
    ci = None)
ax.set(ylabel="",
       xlabel="Count")
sns.despine(left=True, bottom=True)

# Save barchart
f.savefig('img/barchart.png', bbox_inches='tight')

# Initialize the matplotlib figure for time-series plot ----
f, ax = plt.subplots(figsize=(15, 7))

sns.lineplot(
    x="date", 
    y="count",
    data=calls_per_day_table[calls_per_day_table.date != calls_per_day_table.date.max()])
ax.set(ylim=(0, None))

# Save time-series plot
f.savefig('img/time_series_plot.png', bbox_inches='tight')