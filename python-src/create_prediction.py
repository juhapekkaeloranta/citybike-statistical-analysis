import pandas as pd
import sys, os
#import matplotlib.pyplot as plt
#import numpy as np
import datetime
#from sklearn.linear_model import LinearRegression
#from sklearn.cross_validation import train_test_split

from model import assignModelVariables, createAndTrainLinearModel
from read_history_data import readData, getTimeStampFromTmarkedTime
from get_weather_forecast import CURRENTWEATHERFORECASTFILE, fetchAndWriteWeatherForecast

sys.path.append(os.path.realpath('..'))

AVAIL_CURRENT_FILE = 'prediction/dummystations_20181001T040001Z.json'
PREDICTION_OUT_FILE = 'prediction/prediction-' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.csv'

print('\n* PREDICTION CREATION *')

# Read in data
weatherData, bikeData = readData()

# Merge the data into one dataframe
combined = pd.merge(left=bikeData, left_on='time', right=weatherData, right_on='datetime')
combined = combined.dropna()

X, y = assignModelVariables(combined)
linearModel = createAndTrainLinearModel(X, y)

# Get current bike availability NOT IMPLEMENTED

def addTimeColumns(df):
    df['hour'] = df['Time'].apply(lambda x: getTimeStampFromTmarkedTime(x).hour)
    df['month'] = df['Time'].apply(lambda x: getTimeStampFromTmarkedTime(x).month)
    return df

# Fetch and read in current weather prediction for the next 24 hours
fetchAndWriteWeatherForecast()
currentWeatherPred = pd.read_csv(CURRENTWEATHERFORECASTFILE).iloc[0:25,:]
#print(currentWeatherPred)
#print('Current weather prediction shape ', currentWeatherPred.shape)

paramsForNext24h = addTimeColumns(currentWeatherPred).drop('Time', axis=1)
paramsForNext24h.rename(columns={'RainAmountPred': 'rainIntensity_mmh', 'TemperaturePred': 'temperature_c'}, inplace=True)  
print(paramsForNext24h)

#y_pred_next24h = linearModel.predict(paramsForNext24h)
#predictionForNext24h = paramsForNext24h.insert(len(y_pred_next24h.columns), 'Availability', y_pred_next24h)
#print(y_pred_next24h)

# Export the prediction to a csv file
#y_pred_df = pd.DataFrame(y_pred)
#y_pred_df.to_csv(PREDICTION_OUT_FILE)
