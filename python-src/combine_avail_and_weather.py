import pandas as pd
import sys, os
import matplotlib.pyplot as plt

sys.path.append(os.path.realpath('..'))

avail_data = "data/03-hourly-avg-all-stations/hourly-avg-2017-06-all-stations.csv"

weather_data = "weather-data/fmi-raindata-Helsinki-Kaisaniemi-2017-06.csv"

A = pd.read_csv(avail_data, sep=',')
B = pd.read_csv(weather_data, sep=',')
 
A['Sade'] = B['Sade']

print('Please see df A for with column:')
print('timehour  sumofhourlyavg  Sade')