import pandas as pd
import sys, os
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns
import model

currentWeatherData = pd.read_csv('prediction/weatherforecast-HelsinkiKaisaniemi-current.csv', sep=',')
currentWeatherData['Time'] = currentWeatherData['Time'].apply(lambda x: x.split("T")[1])
currentWeatherData['Time'] = currentWeatherData['Time'].apply(lambda x: int(x.split(":")[0]))

preds, _ , _ = model.readStationDataAndTrainPredictors()
BikeAvailabilityPredictionsFromCurrentWeather()

predictionsTable = np.zeros((24,len(preds.items())))
current_col = 0
dfLabels = []
for stationID, pred in preds.items():
    dfLabels += [str(stationID)]
    for i in range(2,26):
        predictionsTable[i-2][current_col] = pred.predict(currentWeatherData['TemperaturePred'].values[i], currentWeatherData['RainAmountPred'].values[i], currentWeatherData['Time'].values[i])
    current_col += 1

predsDF = pd.DataFrame(predictionsTable)
predsDF.to_csv('prediction/BikeAvailability24HourForecast.csv', header=dfLabels)
