import pandas as pd
import sys, os
import matplotlib.pyplot as plt

sys.path.append(os.path.realpath('..'))
filename = "data/04-hour-of-day/hour_of_day-avg.csv"

df=pd.read_csv(filename, sep=',')

#cond = df[df.station == 1]

def plotXY(x_values, y_values):
  plt.plot(x_values, y_values)
  plt.ylabel('some numbers')
  plt.show()

def filterByStation(data, stationID):
    return data[data.station == stationID]

stationIDs = df.station.unique()

for stationID in stationIDs[0:2]:
    dataForStation = filterByStation(df, stationID)
    avgs = dataForStation.avg_availability
    hours = dataForStation.hour_of_day
    plt.figure(stationID)
    plt.plot(hours, avgs)
    plt.xlabel("station: " + str(stationID))
    outputfilename = "img/station_" + str(stationID) + ".png"
    plt.savefig(outputfilename, bbox_inches='tight') 

