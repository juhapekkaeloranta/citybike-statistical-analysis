import pandas as pd
import sys, os
import numpy as np
import datetime
from conversion import getTimeStampFromBikedataTimeHour, getTimeStampFromTmarkedTime, getTimeStampFromWeatherdataTime

AVAIL_DATA_HISTORY_FILES = ['data/02-hourly-avg/bikeAvailability-2017-06-hourly-avg-per-station.csv',
'data/02-hourly-avg/bikeAvailability-2017-08-hourly-avg-per-station.csv', 
'data/02-hourly-avg/bikeAvailability-2017-09-hourly-avg-per-station.csv']
WEATHER_DATA_HISTORY_FILES = ['weather-data/fmi-weatherdata-Helsinki-Kaisaniemi-2016.csv',
'weather-data/fmi-weatherdata-Helsinki-Kaisaniemi-2017.csv', 
'weather-data/fmi-weatherdata-Helsinki-Kaisaniemi-2018.csv']

def readWeatherData():
    print('\n  Reading in historical weather data...')
    # Read in data
    df_from_each_weatherfile = (pd.read_csv(f, sep=",") for f in WEATHER_DATA_HISTORY_FILES)
    weatherData = pd.concat(df_from_each_weatherfile, ignore_index=True)

    weatherData.rename(columns={'Vuosi': 'Year', 'Kk': 'Month', 'Pv': 'Day', 'Klo': 'HourMin', 'Aikavyöhyke': 'Timezone', 'Sateen intensiteetti (mm/h)': 'rainIntensity_mmh', 'Ilman lämpötila (degC)': 'temperature_c'}, inplace=True)  
    weatherData = weatherData.reset_index(drop=True)
    
    # Filter only June, August and September 2017, which we have bike availability data from
    weatherData = weatherData[
        ((weatherData.Year == 2017) & (weatherData.Month.isin([6, 8, 9]))) 
        # ADD THE NEW MONTHS HERE AS OR-CONDITIONS
        #| ((weatherData.Year == 2016) & (weatherData.Month.isin([7, 8, 9])))
        ]
    # Create new datetime column in weatherData combining the time data in separate columns
    weatherData['datetime'] = weatherData.apply(lambda row: str(getTimeStampFromWeatherdataTime(row)), axis=1)

    print('  Historical weather data read and processed.')
    return weatherData

def readBikeData():
    print('\n  Reading in historical bike availability data for model creation...')
    # Read in data
    df_from_each_bikefile = (pd.read_csv(f) for f in AVAIL_DATA_HISTORY_FILES)
    bikeData = pd.concat(df_from_each_bikefile, ignore_index=True)

    # Sort bikedata by date
    bikeData = bikeData.sort_values(by=['time', 'stationid'])
    bikeData = bikeData.reset_index(drop=True)

    print('  Historical bike availability data read and processed.')
    return bikeData