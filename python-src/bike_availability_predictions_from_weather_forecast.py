import pandas as pd
import sys, os
import numpy as np
import datetime
from enum import Enum

from convert_weatherdata_to_historical_forecast import HISTORYWEATHERFORECASTOUTFILE
from model import readStationDataAndTrainPredictors

AVAILABILITYFORECASTOUTFILE = 'prediction/BikeAvailability24HourForecast-' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.csv'
CURRENTAVAILABILITYFORECASTFILE = 'prediction/BikeAvailability24HourForecast-current.csv'
AVAILABILITYOLDFORECASTOUTFILE = 'prediction/BikeAvailability24HourForecast-' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.csv'
CURRENTOLDAVAILABILITYFORECASTFILE = 'prediction/BikeAvailability24HourForecast-12h-old-current.csv'
HISTORICALAVAILABILITYFORECASTFILE = 'prediction/BikeAvailability24HourForecast-historical.csv'

class ForecastType(Enum):
    CURRENT = 'current'
    TWELVEHOURSOLD = 'twelveHoursOld'

def createPrediction(currentWeatherData, preds, forecastType):
    if (forecastType == ForecastType.CURRENT):
        forecastOutFile = AVAILABILITYFORECASTOUTFILE
        currentOutFile = CURRENTAVAILABILITYFORECASTFILE
    elif (forecastType == ForecastType.TWELVEHOURSOLD):
        forecastOutFile = AVAILABILITYOLDFORECASTOUTFILE
        currentOutFile = CURRENTOLDAVAILABILITYFORECASTFILE
    else:
        raise TypeError('Parameter forecastType must be an instance of ForecastType Enum')
    
    print('\nCreating and writing out prediction for all stations...')
    currentWeatherData['Hour'] = currentWeatherData['Time'].apply(lambda x: x.split("T")[1])
    currentWeatherData['Hour'] = currentWeatherData['Hour'].apply(lambda x: int(x.split(":")[0]))

    predictionsTable = np.zeros((25,len(preds.items())))
    current_col = 0
    dfLabels = []
    for stationID, pred in preds.items():
        dfLabels += [str(stationID)]
        for i in range(0,25):
            predictionsTable[i][current_col] = pred.predict(currentWeatherData['TemperaturePred'].values[i], currentWeatherData['RainAmountPred'].values[i], currentWeatherData['Hour'].values[i])
        current_col += 1

    predsDF = pd.DataFrame(predictionsTable, columns = dfLabels)

    # Add timestamp column to the predsDF table
    predsDF.insert(0,'Time', currentWeatherData.loc[0:25,'Time'])

       
    # Disabled: write bike availability forecast to a timestamped file. Uncomment next line to enable.
    #predsDF.to_csv(forecastOutFile, index=False)
    predsDF.to_csv(currentOutFile, index=False)
    print('Prediction created.')

def createHistoricalPrediction(historicalWeatherData, preds):
    print('\nCreating and writing out historical predictions for all stations...')
    historicalWeatherData['Hour'] = historicalWeatherData['Time'].apply(lambda x: x.split("T")[1])
    historicalWeatherData['Hour'] = historicalWeatherData['Hour'].apply(lambda x: int(x.split(":")[0]))

    predictionsTable = np.zeros((len(historicalWeatherData['Time']),len(preds.items())))
    current_col = 0
    dfLabels = []
    for stationID, pred in preds.items():
        dfLabels += [str(stationID)]
        for i in range(0,len(historicalWeatherData['Time'])):
            predictionsTable[i][current_col] = pred.predict(historicalWeatherData['TemperaturePred'].values[i], historicalWeatherData['RainAmountPred'].values[i], historicalWeatherData['Hour'].values[i])
        current_col += 1

    predsDF = pd.DataFrame(predictionsTable, columns = dfLabels)

    # Add timestamp column to the predsDF table
    predsDF.insert(0,'Time', historicalWeatherData.loc[:,'Time'])

    predsDF.to_csv(HISTORICALAVAILABILITYFORECASTFILE, index=False)
    print('Historical predictions created.')

if __name__ == "__main__":
    historyWeatherPred = pd.read_csv(HISTORYWEATHERFORECASTOUTFILE)
    predictors, _ , _ = readStationDataAndTrainPredictors()
    createHistoricalPrediction(historyWeatherPred, predictors)
    
    
