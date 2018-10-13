import pandas as pd
import sys, os
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns

AVAILABILITYFORECASTOUTFILE = 'prediction/BikeAvailability24HourForecast-' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.csv'
CURRENTAVAILABILITYFORECASTFILE = 'prediction/BikeAvailability24HourForecast-current.csv'
HISTORICALAVAILABILITYFORECASTFILE = 'prediction/BikeAvailability24HourForecast-historical.csv'

def createPrediction(currentWeatherData, preds):
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

    predsDF.to_csv(AVAILABILITYFORECASTOUTFILE, index=False)
    predsDF.to_csv(CURRENTAVAILABILITYFORECASTFILE, index=False)
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
