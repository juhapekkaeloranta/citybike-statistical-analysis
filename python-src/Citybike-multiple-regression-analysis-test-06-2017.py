
# coding: utf-8

# ### Citybike statistical analysis with multiple linear regession (test)

import pandas as pd
import sys, os
import matplotlib.pyplot as plt
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression

sys.path.append(os.path.realpath('..'))

avail_data_file = "data/03-hourly-avg-all-stations/hourly-avg-2017-06-all-stations.csv"
weather_data_file = "weather-data/fmi-weatherdata-Helsinki-Kaisaniemi-2017.csv"
prediction_out_file = "prediction/prediction-based-on-2017-06.csv"

# ##### Read and combine data
bikeData = pd.read_csv(avail_data_file, sep=',')
weatherData = pd.read_csv(weather_data_file, sep=",")

weatherData.rename(columns={'Vuosi': 'Year', 'Kk': 'Month', 'Pv': 'Day', 'Klo': 'Time', 'Aikavyöhyke': 'Timezone', 'Sateen intensiteetti (mm/h)': 'rainIntensity_mmh', 'Ilman lämpötila (degC)': 'temperature_c'}, inplace=True)  

# Filter only June 2017
weatherData = weatherData[weatherData.Month == 6]

# Reset dataframe indices to make combining work properly
bikeData = bikeData.reset_index(drop=True)
weatherData = weatherData.reset_index(drop=True)

bikeData['rainIntensity_mmh'] = weatherData['rainIntensity_mmh']
bikeData['temperature_c'] = weatherData['temperature_c']

# ##### Assigning 'sumofhourlyavg' as the dependent variable y
# ##### Assigning 'Sade' and 'Ilman_lampotila' as independent variables X (X is 2xn matrix here but it will still need the weekday-info and hour-columns to be complete)

X = bikeData.loc[:, ['rainIntensity_mmh','temperature_c']] # matrix of independent variables 'rainIntensity_mmh' and 'temperature_c'
y = bikeData[bikeData.columns[1]] # vector of 'sumofhourlyavg'

# Add hour to the matrix of independent variables
X['hour'] = bikeData['timehour'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").hour)

# Add month to the matrix of independent variables
X['month'] = bikeData['timehour'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").month)

# Add weekday to the matrix of independent variables. 0 is Monday, 6 is Sunday.
X['weekday'] = bikeData['timehour'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").weekday())

#print("Variables, row 1: ")
print(X)

# ##### Splitting the dataset 'A' into the Training set and Test set

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state = 0) # 144 (0.2) observations to test-set and 576 (0.8) observations to the train-set

# Feature scaling

# ##### Fitting Multiple Linear Regression to the Training set

# Creating a regressor object of LinearRegression class
regressor = LinearRegression()

# Applying fit-method to the training set
regressor.fit(X_train, y_train)

# ##### Testing the performance of multiple linear regression model (predicting test set results)
y_pred = regressor.predict(X_test)

# ##### Checking how well the linear regression model fits to the observations
R_2 = regressor.score(X_train, y_train)
print(R_2)  # 0.015354948259910128  

# ##### R-squared is the statistical measure that tells how close the data are to the fitted regression line. The value range is from 0 to 1 where 1 would mean perfect fit and 0 represents a model that does not explain any of the variation in the response variable. So in this case, especially when needed to apply hardcoding for replacing quickly the temperature variable's nulls, the model ended up only 0,015 so only 1,5%. The rule of thumb: the larger the R**2, the better the regression model fits to the observations

# Exporting the prediction-vector y_pred to a csv-file

y_pred_df = pd.DataFrame(y_pred)

# The file currently being written out is meaningless (the prediction on a randomly selected subset of hours from 2017-06.)
y_pred_df.to_csv(prediction_out_file)

