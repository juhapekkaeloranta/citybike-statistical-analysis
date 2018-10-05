import csv, json
import os
import pandas as pd

from get_weather_forecast import CURRENTWEATHERFORECASTFILE, fetchAndWriteWeatherForecast
from bike_availability_predictions_from_weather_forecast import CURRENTAVAILABILITYFORECASTFILE, createPrediction
from model import readStationDataAndTrainPredictors
import server

AVAIL_CURRENT_FILE = 'data/01-raw-datadummystations_20181001T040001Z.json'

class Controller():
    def __init__(self):
        self.predictors = self.createPredictionModel()
        
    def createPredictionModel(self):
        """ Create stationwise prediction models, train them on historical data and return them """
        print('\nCreating model...')
        predictors, _ , _ = readStationDataAndTrainPredictors()
        print('\nModel created and trained.')
        return predictors

    def readCurrentAvailabilityPrediction(self):
        pred = pd.read_csv(CURRENTAVAILABILITYFORECASTFILE)
        print('\nCurrent availability prediction: \n', pred)
        return pred

    def convertPredictionToJSON(self, pred):
        # NOT IMPLEMENTED YET
        return pred

    def createAvailabilityPredictionForAllStations(self):
        """Create availability prediction for all stations for the next 24 hours. Return in JSON format
        with each object a single prediction for station id and time."""
    
        # Fetch latest weather forecast and write it to disk
        fetchAndWriteWeatherForecast()

        # Read in current weather forecast
        currentWeatherPred = pd.read_csv(CURRENTWEATHERFORECASTFILE)

        # Get current bike availability data
        # NOT IMPLEMENTED

        # Create stationwise predictions for the next 24 hours and write them to disk
        print('\nCreating prediction for all stations...')
        createPrediction(currentWeatherPred, self.predictors)
        print('Prediction created.')

        currentPrediction = self.readCurrentAvailabilityPrediction()
        currentPredictionJSON = self.convertPredictionToJSON(currentPrediction)
        
        return currentPredictionJSON

def main():
    print('*** Citybike predictor ***')
    print('\nBackend started from controller.py.')
    controller = Controller()
    pred = controller.createAvailabilityPredictionForAllStations()

if __name__ == "__main__":
    main()
