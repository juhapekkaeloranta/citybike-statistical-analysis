import pandas as pd
from datetime import datetime
import time
import sys, os
import matplotlib.pyplot as plt
from constants import stationIds

sys.path.append(os.path.realpath('..')) 

startDate = '09/1/2018'
days = 30
filetime = '2018-09'
filename = 'data/01-raw-data/raw-bikeAvailability-' + filetime + '.csv'
outfilename = 'data/02-hourly-avg/bikeAvailability-' + filetime + '-hourly-avg-per-station.csv'

df = pd.read_csv(filename)
#df = pd.read_csv('data/01-raw-data/minutely-data-sample.csv')

print('CSV read. Size:')
print(df.size)

stations = pd.DataFrame({'stationid': stationIds})

def roundTimestampToHour(strTimestamp):
    dt = datetime.strptime(strTimestamp, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(minute=0, second=0, microsecond=0)
    return dt
    
df['time'] = df.apply( lambda row: roundTimestampToHour(row['time']) , axis=1 )

print('time rounded:')
print(df[0:5])

hourlyAvg = df.groupby(['stationid', 'time']).mean().round(decimals=1)

print('AVG, group by:')
print(hourlyAvg[0:5])

'''
Data is missing some rows. I.e. no data for some hours at all!
To handle this, we create a matrix with 107280 (149*30*24=107280, stations*days*hours) rows with columns
stationId,timestamp
This matrix is then combined with actual data with a join operation
'''

def buildDateRangeDf(beginDate, days):
    return pd.DataFrame({'time': pd.date_range(beginDate, periods=days*24, freq='H')})

def cartesianProduct(A, B):
    # Full join for two dataframes without common columns
    A['tmp'] = 1
    B['tmp'] = 1
    merged = A.merge(monthHours, how='outer')
    merged = merged.drop(['tmp'], axis=1)
    return merged

print('merging..')
monthHours = buildDateRangeDf(startDate, days)
stationsXtimestamps = cartesianProduct(stations, monthHours)

ready_df = pd.merge(stationsXtimestamps, hourlyAvg,  how='left', left_on=['stationid','time'], right_on = ['stationid','time'])

print('Saving file..')
ready_df.to_csv(outfilename, index=False, na_rep="NaN")
print('Done!')