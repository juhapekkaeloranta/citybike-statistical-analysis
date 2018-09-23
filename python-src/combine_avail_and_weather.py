import pandas as pd
import sys, os
import matplotlib.pyplot as plt

sys.path.append(os.path.realpath('..'))

avail_data_file = "data/03-hourly-avg-all-stations/hourly-avg-2017-06-all-stations.csv"
weather_data_file = "weather-data/fmi-weatherdata-Helsinki-Kaisaniemi-2017.csv"
combined_data_out_file = "combined-data/combined-data-2017-06.csv"

A = pd.read_csv(avail_data_file, sep=',')
B = pd.read_csv(weather_data_file, sep=',')

# Filter only the rows for the month 2017-06 from the year 2017 weather data
B = B[B.Kk ==6]

# Reset dataframe indices to make combining work properly
A = A.reset_index(drop=True)
B = B.reset_index(drop=True)

A['rainAmount'] = B['Sateen intensiteetti (mm/h)']
A['temperature'] = B['Ilman lämpötila (degC)']

#print('Please see df A for with column:')
#print('timehour  sumofhourlyavg  rainAmount temperature')

A.to_csv(combined_data_out_file, index=False)
