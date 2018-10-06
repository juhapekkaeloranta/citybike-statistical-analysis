import pandas as pd
import sys, os
import numpy as np
import datetime


AVAIL_DATA_HISTORY_FILES = ['data/02-hourly-avg/bikeAvailability-2017-06-hourly-avg-per-station.csv',
'data/02-hourly-avg/bikeAvailability-2017-08-hourly-avg-per-station.csv', 
'data/02-hourly-avg/bikeAvailability-2017-09-hourly-avg-per-station.csv']
WEATHER_DATA_HISTORY_FILE = 'weather-data/fmi-weatherdata-Helsinki-Kaisaniemi-2017.csv'

def readData():
    print('\n  Reading in history data for model creation...')
    # Read in data
    df_from_each_bikefile = (pd.read_csv(f) for f in AVAIL_DATA_HISTORY_FILES)
    bikeData   = pd.concat(df_from_each_bikefile, ignore_index=True)

    weatherData = pd.read_csv(WEATHER_DATA_HISTORY_FILE, sep=",")
    weatherData.rename(columns={'Vuosi': 'Year', 'Kk': 'Month', 'Pv': 'Day', 'Klo': 'HourMin', 'Aikavyöhyke': 'Timezone', 'Sateen intensiteetti (mm/h)': 'rainIntensity_mmh', 'Ilman lämpötila (degC)': 'temperature_c'}, inplace=True)  
    weatherData = weatherData.reset_index(drop=True)
    
    # Filter only June, August and September 2017, which we have bike availability data from
    weatherData = weatherData[weatherData.Month.isin([6, 8, 9])]

    # Sort bikedata by date
    bikeData = bikeData.sort_values(by=['time', 'stationid'])
    bikeData = bikeData.reset_index(drop=True)

    # Create new datetime column in weatherData combining the time data in separate columns
    weatherData['datetime'] = weatherData.apply(lambda row: str(getTimeStampFromWeatherdataTime(row)), axis=1)

    print('  History data read and processed.')
    return weatherData, bikeData

def getTimeStampFromBikedataTimeHour(time):
    return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

def getTimeStampFromWeatherdataTime(row):
    return datetime.datetime(year=int(row.Year), month=int(row.Month), day=int(row.Day), hour=int(row.HourMin.split(':')[0]), minute=int(row.HourMin.split(':')[1]))

def getTimeStampFromTmarkedTime(time):
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")