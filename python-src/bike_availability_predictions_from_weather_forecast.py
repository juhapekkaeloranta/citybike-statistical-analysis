import pandas as pd
import sys, os
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns
import model

os.chdir('/home/mkotola/IntroDataS/citybike-statistical-analysis')
print(os.getcwd())

AVAILABILITYFORECASTOUTFILE = 'prediction/BikeAvailability24HourForecast-' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.csv'
CURRENTAVAILABILITYFORECASTFILE = 'prediction/BikeAvailability24HourForecast-current.csv'

currentWeatherData = pd.read_csv('prediction/weatherforecast-HelsinkiKaisaniemi-current.csv', sep=',')
currentWeatherData['Hour'] = currentWeatherData['Time'].apply(lambda x: x.split("T")[1])
currentWeatherData['Hour'] = currentWeatherData['Hour'].apply(lambda x: int(x.split(":")[0]))

preds, _ , _ = model.readStationDataAndTrainPredictors()

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

predsDF.to_csv(AVAILABILITYFORECASTOUTFILE)
predsDF.to_csv(CURRENTAVAILABILITYFORECASTFILE)