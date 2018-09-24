import pandas as pd
from datetime import datetime
import time
import sys, os
import matplotlib.pyplot as plt
from constants import stationIds

sys.path.append(os.path.realpath('..')) 

df = pd.read_csv('data/01-raw-data/raw-bikeAvailability-2017-08.csv')
#df = pd.read_csv('data/01-raw-data/minutely-data-sample.csv')

stations = pd.DataFrame({'stationid': stationIds})

def roundTimestampToHour(strTimestamp):
    dt = datetime.strptime(strTimestamp, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(minute=0, second=0, microsecond=0)
    return dt
    
df['time'] = df.apply( lambda row: roundTimestampToHour(row['time']) , axis=1 )

hourlyAvg = df.groupby(['stationid', 'time']).mean().round(decimals=1)

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

monthHours = buildDateRangeDf('08/1/2017', 31)
stationsXtimestamps = cartesianProduct(stations, monthHours)

ready_df = pd.merge(stationsXtimestamps, hourlyAvg,  how='left', left_on=['stationid','time'], right_on = ['stationid','time'])

ready_df.to_csv('bikeAvailability-2017-08-hourly-avg-per-station.csv', index=False, na_rep="NaN")