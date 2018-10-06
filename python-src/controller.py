import csv, json
import os
import pandas as pd

os.chdir('/home/mkotola/IntroDataS/citybike-statistical-analysis')
print('Current working dir: ', os.getcwd())

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
        currentPredictionJSON = json.dumps(self.convertPredictionToJSON(currentPrediction))
        #print(currentPredictionJSON)
        return currentPredictionJSON

def main():
    print('\n*** Citybike predictor ***')
    print('\nBackend started from controller.py.')
    controller = Controller()
    pred = controller.createAvailabilityPredictionForAllStations()

if __name__ == "__main__":
    main()
