import pandas as pd
import sys, os
import numpy as np
import datetime
import conversion

HISTORYWEATHERFORECASTOUTFILE = 'prediction/weatherforecast-HelsinkiKaisaniemi-history.csv'

def convertWeatherdataToHistoricalForecast():
    weatherData = read_history_data.readWeatherData()

    weatherData.drop(columns=['Year', 'Month', 'Day', 'HourMin', 'Timezone'])
    weatherData = weatherData[['datetime', 'rainIntensity_mmh', 'temperature_c']]
    weatherData.columns = ['Time','RainAmountPred','TemperaturePred']
    weatherData['Time'] = weatherData['Time'].apply(lambda timestamp: conversion.getUTCTimeStampFromTimeStamp(timestamp))
    #print(weatherData)

    weatherData.to_csv(HISTORYWEATHERFORECASTOUTFILE, index=False)
    print('  Wrote historical weather forecasts to disk.')

if __name__ == "__main__":
    convertWeatherdataToHistoricalForecast()
