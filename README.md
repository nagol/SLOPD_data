# SLOPD Call Log Data

## Project Goal: 
  + Pull and parse the daily San Luis Obispo Police Department call logs 
  + Automate the process with Github Actions
  + Build up an interesting data table of police call activity over time

### Data Source:
https://www.slocity.org/government/department-directory/police-department/police-log

According to the website, the data is updated by 3PM Monday - Thursday. The Monday data contains all of the weekend data as well.

### Current State

[![scraper-slopd](https://github.com/nagol/SLOPD_data/actions/workflows/main.yml/badge.svg)](https://github.com/nagol/SLOPD_data/actions/workflows/main.yml)

[![create_plots](https://github.com/nagol/SLOPD_data/actions/workflows/create_plots.yml/badge.svg)](https://github.com/nagol/SLOPD_data/actions/workflows/create_plots.yml)


### Data - Quick Look

#### Number of Calls per Day Captured

![](../main/img/time_series_plot.png)


#### Breakdown of Call Types

![](../main/img/barchart.png)
