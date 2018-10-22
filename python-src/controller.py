import csv, json
import os, sys
import pandas as pd
import datetime

from get_weather_forecast import CURRENTWEATHERFORECASTFILE, fetchAndWriteWeatherData, WeatherDataType
from bike_availability_predictions_from_weather_forecast import CURRENTAVAILABILITYFORECASTFILE, HISTORICALAVAILABILITYFORECASTFILE, createPrediction, createHistoricalPrediction
from convert_weatherdata_to_historical_forecast import HISTORYWEATHERFORECASTOUTFILE
from model import readStationDataAndTrainPredictors
import read_history_data
import conversion

AVAIL_CURRENT_FILE = 'data/01-raw-datadummystations_20181001T040001Z.json'
INTERVAL_FOR_NEW_PREDICTIONS = 60 # in seconds

class Controller():
    def __init__(self):
        self.predictors = self.createPredictionModel()
        self.latestPredictionUpdateTime = datetime.datetime(2000, 1, 1)
        self.updateWeatherAndAvailabilityPredictions()
        self.latestPredictionUpdateTime = datetime.datetime.now()
        self.historyPrediction = {}
        self.bikeAvailabilityHistory = {}
        self.historyLoaded = False
        pd.options.mode.chained_assignment = None
        
    def createPredictionModel(self):
        """ Create stationwise prediction models, train them on historical data and return them """
        print('\nCreating model...')
        predictors, _ , _ = readStationDataAndTrainPredictors()
        print('\nModel created and trained.')
        return predictors

    def readCurrentAvailabilityPrediction(self):
        return pd.read_csv(CURRENTAVAILABILITYFORECASTFILE)
        
    def readHistoricalAvailabilityPrediction(self):
        return pd.read_csv(HISTORICALAVAILABILITYFORECASTFILE)
    
    def createHistoricalAvailabilityPrediction(self):
        historyWeatherPred = pd.read_csv(HISTORYWEATHERFORECASTOUTFILE)
        createHistoricalPrediction(historyWeatherPred, self.predictors)

    def getTimeLimits(self, centreTime):
        centreDateTime = datetime.datetime.strptime(centreTime, "%Y-%m-%dT%H:%M:%SZ")
        startDateTime = centreDateTime - datetime.timedelta(hours=12)
        endDateTime = centreDateTime + datetime.timedelta(hours=12)
        return startDateTime, centreDateTime, endDateTime

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
        timeFromLastUpdate = (datetime.datetime.now() - self.latestPredictionUpdateTime).total_seconds()
        print('Time difference from last update in seconds: ', timeFromLastUpdate)
        if (timeFromLastUpdate > INTERVAL_FOR_NEW_PREDICTIONS):
            print('Updating predictions...')
            # Fetch latest weather forecast, write it to disk and read it back in
            fetchSuccess = fetchAndWriteWeatherData(WeatherDataType.FORECAST)
            
            if fetchSuccess:
                currentWeatherPred = pd.read_csv(CURRENTWEATHERFORECASTFILE)
            
                # Create stationwise predictions for the next 24 hours and write them to disk
                createPrediction(currentWeatherPred, self.predictors)
                self.latestPredictionUpdateTime = datetime.datetime.now()
                print('Predictions updated.')
            else:
                print('Predictions not updated.')
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

    # HISTORICAL DATA METHODS

    def createSingleHistoryJSONObject(self, stationid, time, avlBikes, prediction):
        JSONItem = {}
        JSONItem["stationid"] = stationid
        JSONItem["time"] = time
        JSONItem["avlBikes"] = avlBikes
        JSONItem["prediction"] = prediction
        return JSONItem
            
    def convertCombinedToJSON(self, combined):
        predictionPoints = []
        for index, row in combined.iterrows():
            predictionPoints.append(self.createSingleHistoryJSONObject(row["stationid"], row["Time"], row["avlbikes"], row["prediction"]))
        return predictionPoints
    
    def getHistoryDataForAllStations(self, centreTime):
        bikeAvailabilityHistory = read_history_data.readBikeData()
        # Convert column time from string format to actual timestamps
        bikeAvailabilityHistory['time'] = pd.to_datetime(bikeAvailabilityHistory['time'])

        startDateTime, centreDateTime, endDateTime = self.getTimeLimits(centreTime)

        bikeAvailabilityHistory = bikeAvailabilityHistory[ 
            (bikeAvailabilityHistory.time <= endDateTime) &
            (bikeAvailabilityHistory.time >= startDateTime)]
        bikeAvailabilityHistory = bikeAvailabilityHistory.reset_index(drop=True)
        return bikeAvailabilityHistory

    def loadHistory(self):
        print('Fetching history data to controller memory...')
        self.historyPrediction = self.readHistoricalAvailabilityPrediction()
        self.historyPrediction.loc[:,'Time'] = pd.to_datetime(self.historyPrediction['Time'])
            
        self.bikeAvailabilityHistory = read_history_data.readBikeData()
        self.bikeAvailabilityHistory['time'] = pd.to_datetime(self.bikeAvailabilityHistory['time'])
        
        self.historyLoaded = True
        print('History data fetched to controller memory.')

    def getHistoryDataForOneStation(self, stationid, centreTime):
        startDateTime, centreDateTime, endDateTime = self.getTimeLimits(centreTime)

        bikeAvailabilityHistory = self.bikeAvailabilityHistory.copy(deep=True)
        bikeAvailabilityHistory = bikeAvailabilityHistory[(bikeAvailabilityHistory['stationid'] == stationid) & 
            (bikeAvailabilityHistory.time <= centreDateTime) &
            (bikeAvailabilityHistory.time >= startDateTime)]
        bikeAvailabilityHistory = bikeAvailabilityHistory.reset_index(drop=True)
        return bikeAvailabilityHistory
    
    def getHistoryAvailabilityPredictionForOneStation(self, stationidStr, centreTime):
        """Returns historical availability prediction for one station for +-12 hours from given time in JSON format
        with each object a single prediction for station id and time. Includes actual data from -12 hours to given time."""

        stationid = int(stationidStr) 
        
        # Only read in history predictions once and store in controller's memory
        #print('Truth value: ', not self.historyPredictionLoaded)
        if not (self.historyLoaded):
            self.loadHistory()
        
        historyPrediction = self.historyPrediction.copy(deep=True)
        historyPrediction = historyPrediction[['Time', str(stationid)]]        
        startDateTime, centreDateTime, endDateTime = self.getTimeLimits(centreTime)

        historyPrediction = historyPrediction[ 
            (historyPrediction.Time <= endDateTime) &
            (historyPrediction.Time >= startDateTime)]
        
        historyPrediction['Time'] = historyPrediction['Time'].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        historyPrediction = historyPrediction.reset_index(drop=True)
                
        historyDataForOneStation = self.getHistoryDataForOneStation(stationid, centreTime)
        historyDataForOneStation['time'] = historyDataForOneStation['time'].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Merge the data into one dataframe and reformat to match API requirements
        combined = pd.merge(left=historyPrediction, left_on='Time', right=historyDataForOneStation, right_on='time', how='outer',)
        combined = combined.drop(columns=['time'])
        combined = combined.rename(index=str, columns={str(stationid): "prediction"})
        combined['stationid'].fillna(stationid, inplace=True)
        combined['avlbikes'].fillna(-1, inplace=True)
        combined['avlbikes'].replace({-1: None}, inplace=True)
        combined['stationid'] = combined['stationid'].astype(int, inplace=True).apply(str)
        combined['prediction'] = combined['prediction'].round(2)
        
        historyPredictionJSON = json.dumps(self.convertCombinedToJSON(combined))
        return historyPredictionJSON
        
def main():
    print('\n*** Citybike predictor ***')
    print('\nBackend started from controller.py.')
    controller = Controller()
    
    # Get availability forecasts for all stations for the next 24 hours.
    #pred = controller.getAvailabilityPredictionForAllStations()
    
    # Here you can update all historical availability predictions. If you have new weather data,
    # run convert_weatherdata_to_historical_forecast.py before running this.
    #controller.createHistoricalAvailabilityPrediction()

    # Get a sample of combined history data in JSON (as the server API at /combined/2/2017-06-12T22:00:00Z will return it)
    #sampleJSON = controller.getHistoryAvailabilityPredictionForOneStation("2", "2017-06-12T22:00:00Z")
    #print(sampleJSON)

if __name__ == "__main__":
    main()
