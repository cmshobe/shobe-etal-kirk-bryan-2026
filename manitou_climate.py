#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to create Figure 2 in the 2026 Kirk Bryan Field Trip guide (Shobe et al):
    plots climate data from the Rocky Mountain Research Station and the
    National Atmospheric Deposition Program

Created Spring 2026

@author: Charles Shobe, USFS Rocky Mountain Research Station

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(2, 2, figsize = (8,5))
MAT = axs[0, 0]
years = axs[0, 1]
monthly = axs[1, 0]
cumulative = axs[1, 1]

text_x = 0.02
text_y = 0.84

####import USFS climate data from Manitou Experimental Forest 
####(used to generate temperature plot (panel A))

file_name = 'MEF_Met_2025_QAQCd_v2.csv'

# Define the data types for specific columns
data_types = {
    'JDay': 'int32',
    'TA': 'float64',
}

data_hourly = pd.read_csv(str(file_name), header = 0, encoding='ISO-8859-1',
                          skiprows = [1], dtype=data_types)
data_hourly.rename(columns={'ï»¿Year': 'Year'}, inplace=True)

#drop rows where air temp is -9999 (no data)
data_hourly.drop(data_hourly[data_hourly['TA'] <= -9000].index, inplace=True)

#plot annual temperature by year (panel A)

MAT.bar(np.arange(1999, 2025), data_hourly.groupby('Year')['TA'].mean().loc[1999:2024],
        color = 'dimgray')

MAT.set_xlim(1998.2, 2024.8)
MAT.set_ylim(4, 7)
MAT.set_xticks(np.array([2000, 2010, 2020]))

MAT.set_xlabel('Year')
MAT.set_ylabel(r'Mean annual temp. [$^\circ$C]')

MAT_average = data_hourly.groupby('Year')['TA'].mean().loc[1999:2024].mean()

MAT.axhline(MAT_average, color = 'k', linestyle = '-', linewidth = 2,
              label = '1999-2024 average')

MAT.legend(bbox_to_anchor = (0.175, 0.2), loc = 'upper left', 
                        bbox_transform = MAT.transAxes,
                        framealpha = 1, edgecolor = 'k')

MAT.text(text_x, text_y, 'A', transform=MAT.transAxes, fontsize = 20, zorder = 10)



####import NADP DATA 
####(used to generate precipitation plots (panels B-D))

#new, weeks-aggregated code
file_name = 'NTN-co21-w-s-mg.csv'
data_weekly = pd.read_csv(str(file_name), header = 0)
data_weekly['yearmonth_datetime'] = pd.to_datetime(data_weekly['yrmonth'], 
                                                   format = '%Y%m')
data_weekly['year'] = data_weekly['yearmonth_datetime'].dt.year
data_weekly['subppt_floored'] = data_weekly['subppt'].clip(lower=0)


#array to hold values for each week for average line
#structure: rows are years, columns are weeks. make 53 columns (max weeks in any yr)
#45 rows; thats hwo many complete years there are
week_aggregation = np.zeros((47, 53))
week_aggregation[:, :] = np.nan
weekly_averages = np.zeros(53)
weekly_averages[:] = np.nan

#plot each cumulative sum
iter = 0

annual_sums = np.zeros(2025 + 1 - 1979)

for year in data_weekly['year'].unique():
   single_year = data_weekly[(data_weekly['yrmonth'] >= int(str(year - 1) + '10')) 
                                 & (data_weekly['yrmonth'] <= int(str(year) + '09'))].copy()
   if len(single_year) < 26:
       print('not enough weekly data in WY ' + str(year) + ': ' + str(len(single_year)))
   else:
       annual_sums[iter] = single_year['subppt'].sum()
       iter += 1


#plot annual precipitation by year (panel B)
years.bar(np.arange(1979, 1979 + len(annual_sums)), annual_sums, color = 'dimgray')
years.set_xlabel('Water year')
years.set_ylabel('Annual precipitation [mm]')

years.set_xticks(np.arange(1980, 1980 + 2023-1978, 10))
years.set_xticklabels(['1980',
                       '1990',
                       '2000',
                       '2010',
                       '2020'])

years.set_xlim(1978, 2026)

annual_sums_average = np.average(annual_sums)

years.axhline(annual_sums_average, color = 'k', linestyle = '-', linewidth = 2,
              label = 'WY 1979-2025 average')

years.text(text_x, text_y, 'B', transform=years.transAxes, fontsize = 20, zorder = 10)

years.legend(bbox_to_anchor = (0.145, 0.2), loc = 'upper left', 
                        bbox_transform = years.transAxes,
                        framealpha = 1, edgecolor = 'k')

##########################################cumulative trajectories for each year


#array to hold values for each week for average line
#structure: rows are years, columns are weeks. make 53 columns (max weeks in any yr)
#45 rows; that's how many complete years there are
week_aggregation = np.zeros((47, 53))
week_aggregation[:, :] = np.nan
weekly_averages = np.zeros(53)
weekly_averages[:] = np.nan
#plot each cumsum
iter = 0

for year in data_weekly['year'].unique():
   single_year = data_weekly[(data_weekly['yrmonth'] >= int(str(year - 1) + '10')) 
                                 & (data_weekly['yrmonth'] <= int(str(year) + '09'))].copy()
   if len(single_year) < 26:
       print('not enough weekly data in WY ' + str(year) + ': ' + str(len(single_year)))
   else:
       #get single year's week timeseries
       single_year['start_datetime'] = pd.to_datetime(single_year['dateOn'])
       single_year['end_datetime'] = pd.to_datetime(single_year['dateOff'])
       start_time = single_year.iloc[0, -2]
       single_year['days_since_WY_start'] = (single_year['end_datetime'] - start_time).dt.days
       single_year['wy_cumsum'] = single_year['subppt_floored'].cumsum()
       
       if len(single_year) >= 52:
           #make sure there's sufficient data (at least 52 weeks) to bin by week
           week_aggregation[iter, :len(single_year)] = single_year['wy_cumsum']

       
       cumulative.plot(pd.concat([pd.Series([0]), single_year['days_since_WY_start']]), 
                pd.concat([pd.Series([0]), single_year['wy_cumsum']]),
                color = 'lightgray')
       iter += 1

#average across all rows (years) for each week
weekly_averages = np.nanmean(week_aggregation, axis = 0)
days_since_wy_start = np.arange(0, 375, 7)


#plot cumulative precipitation by week (panel D)
cumulative.plot(days_since_wy_start, np.insert(weekly_averages, 0, 0), 
                color = 'k', linewidth = 2, label = 'WY 1979-2025 average')
cumulative.legend(bbox_to_anchor = (0.1, 1.01), loc = 'upper left', 
                        bbox_transform = cumulative.transAxes,
                        framealpha = 1, edgecolor = 'k')

cumulative.set_xlabel('Day of water year')
cumulative.set_ylabel('Cumulative' '\n' 'precipitation [mm]')

cumulative.set_xlim(0, 364)

cumulative.text(text_x, text_y, 'D', transform=cumulative.transAxes, fontsize = 20, zorder = 10)


#use weekly precipitation data to get average monthly precipitation
data_weekly['month'] = data_weekly['yearmonth_datetime'].dt.month
monthly_means = data_weekly.groupby(['month', 'year'])['subppt'].sum()
monthly_means = monthly_means.reset_index()
monthly_means = monthly_means.groupby('month')['subppt'].mean().reset_index()
monthly_means.rename(columns={'subppt': 'average_subppt'}, inplace=True)
monthly_means_rolled = pd.concat([monthly_means.tail(3), monthly_means.head(len(monthly_means) - 3)], ignore_index=True)


#plot average precipitation by month (panel C)

monthly.bar(np.arange(1, 13), monthly_means_rolled['average_subppt'], color = 'dimgray')

monthly.set_xticks(np.arange(1, 13))
monthly.set_xticklabels(['O',
                         'N',
                         'D',
                         'J',
                         'F',
                         'M',
                         'A',
                         'M',
                         'J',
                         'J',
                         'A',
                         'S'])

monthly.set_xlabel('Month of water year')
monthly.set_ylabel('Average monthly''\n''precipitation [mm]')

monthly.set_xlim(0.4, 12.6)

monthly.text(text_x, text_y, 'C', transform=monthly.transAxes, fontsize = 20, zorder = 10)

plt.tight_layout()
fig.savefig('manitou_climate.png', dpi=1000, bbox_inches = 'tight')
fig.savefig('manitou_climate.eps', dpi=1000, bbox_inches = 'tight')