import csv, json
import os
import pandas as pd
import datetime
from datetime import datetime, date, time, timedelta

from get_weather_forecast import CURRENTWEATHERFORECASTFILE, fetchAndWriteWeatherForecast
from bike_availability_predictions_from_weather_forecast import CURRENTAVAILABILITYFORECASTFILE, createPrediction
from model import readStationDataAndTrainPredictors

AVAIL_CURRENT_FILE = 'data/01-raw-datadummystations_20181001T040001Z.json'
INTERVAL_FOR_NEW_PREDICTIONS = 60 # in seconds

class Controller():
    def __init__(self):
        self.predictors = self.createPredictionModel()
        self.latestPredictionUpdateTime = datetime(2000, 1, 1)
        self.updateWeatherAndAvailabilityPredictions()
        self.latestPredictionUpdateTime = datetime.now()
        
    def createPredictionModel(self):
        """ Create stationwise prediction models, train them on historical data and return them """
        print('\nCreating model...')
        predictors, _ , _ = readStationDataAndTrainPredictors()
        print('\nModel created and trained.')
        return predictors

    def readCurrentAvailabilityPrediction(self):
        pred = pd.read_csv(CURRENTAVAILABILITYFORECASTFILE)
        # Uncomment to print current availability prediction
        # print('\nCurrent availability prediction: \n', pred)
        return pred

    def createSingleJSONObject(self, stationid, time, avlBikes):
        JSONItem = {}
        JSONItem["stationid"] = stationid
        JSONItem["time"] = time
        JSONItem["avlBikes"] = avlBikes
        return JSONItem
            
    def convertPredictionToJSON(self, pred):
        predictionPoints = []
        for index, row in pred.iterrows():
            for stationid in pred.columns.values.tolist()[1:]:
                predictionPoints.append(self.createSingleJSONObject(stationid, row["Time"], row[stationid]))
        return predictionPoints

    def updateWeatherAndAvailabilityPredictions(self):
        timeFromLastUpdate = (datetime.now() - self.latestPredictionUpdateTime).total_seconds()
        print('Time difference from last update in seconds: ', timeFromLastUpdate)
        if (timeFromLastUpdate > INTERVAL_FOR_NEW_PREDICTIONS):
            print('Updating predictions...')
            # Fetch latest weather forecast, write it to disk and read it back in
            fetchAndWriteWeatherForecast()
            currentWeatherPred = pd.read_csv(CURRENTWEATHERFORECASTFILE)
            
            # Get current bike availability data
            # NOT IMPLEMENTED

            # Create stationwise predictions for the next 24 hours and write them to disk
            createPrediction(currentWeatherPred, self.predictors)
            print('Predictions updated.')
        else:
            print('No need to update predictions yet.')

    def getAvailabilityPredictionForAllStations(self):
        """Returns availability prediction for all stations for the next 24 hours in JSON format
        with each object a single prediction for station id and time."""

        self.updateWeatherAndAvailabilityPredictions()
        currentPrediction = self.readCurrentAvailabilityPrediction()
        currentPredictionJSON = json.dumps(self.convertPredictionToJSON(currentPrediction))
        return currentPredictionJSON
    
    def getAvailabilityPredictionForOneStation(self, stationid):
        """Returns availability prediction for one station for the next 24 hours in JSON format
        with each object a single prediction for station id and time."""

        self.updateWeatherAndAvailabilityPredictions()
        currentPrediction = self.readCurrentAvailabilityPrediction()
        currentPrediction = currentPrediction[['Time', stationid]]
        currentPredictionJSON = json.dumps(self.convertPredictionToJSON(currentPrediction))
        return currentPredictionJSON
    
    def getAvailabilityPredictionForOneStationHour(self, stationid, timestamp):
        """Returns availability prediction for one station for the next 24 hours in JSON format
        with each object a single prediction for station id and time."""

        self.updateWeatherAndAvailabilityPredictions()
        currentPrediction = self.readCurrentAvailabilityPrediction()
        currentPrediction = currentPrediction[['Time', stationid]]
        currentPrediction = currentPrediction.loc[currentPrediction['Time'] == timestamp]
        currentPredictionJSON = json.dumps(self.convertPredictionToJSON(currentPrediction))
        return currentPredictionJSON

    def getHistoryData(self, stationid, endTime):
        year = datetime.strptime(endTime, "%Y")
        month = datetime.strptime(endTime, "%m")
        df = pd.read_csv("data/02-hourly-avg/bikeAvailability-" + year + "-" + month + "-hourly-avg-per-station.csv")
        df['time'] = pd.to_datetime(df['time'])
        endTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        startTime = endTime - timedelta(hours=25)
        df = df[(df['stationid'] == stationid) & 
            (df.time < endTime) &
            (df.time > startTime)]
        return df

def main():
    print('\n*** Citybike predictor ***')
    print('\nBackend started from controller.py.')
    controller = Controller()
    pred = controller.createAvailabilityPredictionForAllStations()

if __name__ == "__main__":
    main()
