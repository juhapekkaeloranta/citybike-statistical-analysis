import pandas as pd
import sys, os
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns
import read_history_data as rhd

# Useful if the polynomials fit the data poorly, so the predictor would return the average availability for the station
import warnings
warnings.filterwarnings("error")

class BikeAvailabilityPredictor:
    def __init__(self, tempCoeffs, rainCoeffs, hoursCoeffs, maxAvailability):
        self.pCoeffsTemp = tempCoeffs
        self.pCoeffsRain = rainCoeffs
        self.pCoeffsHours = hoursCoeffs
        self.maxAvailability = maxAvailability

    def predict(self, temperature_c, rain_MA, hour):
        return_val = 0
        if (np.isnan(rain_MA) or rain_MA == 0):
            temp_val = np.polyval(self.pCoeffsTemp, temperature_c)
            hour_val = np.polyval(self.pCoeffsHours, hour)
            return_val = 0.29*temp_val + 0.71*hour_val
        else:
            rain_val = np.polyval(self.pCoeffsRain, rain_MA)
            hour_val = np.polyval(self.pCoeffsHours, hour)
            return_val = 0.72*rain_val + 0.28*hour_val + 0.1 # Constant bias 0.1 bikes when raining.
        if return_val > self.maxAvailability:
            return self.maxAvailability
        if return_val < 0 or np.isnan(return_val):
            return 0
        return return_val

def readStationDataAndTrainPredictors():
    weatherData, stationData = rhd.readData()
    weatherData["Time"] = weatherData["HourMin"].apply(lambda x: int(x.split(":")[0]))

    nRows = len(weatherData)

    weatherData['rain_MA'] = np.zeros(nRows)
    moving_average_window_size = 8

    for i in range(nRows):
        avg_val = 0
        sum_count = 0
        for j in range(moving_average_window_size):
            if (i-j >= 0):
                if np.isfinite(weatherData['rainIntensity_mmh'].values[i-j]):
                    avg_val += weatherData['rainIntensity_mmh'].values[i-j] # moving average
                sum_count += 1
        avg_val /= sum_count
        weatherData['rain_MA'].values[i] = avg_val


    stationCount = 0
    predictors = {}
    for i in range(1, np.max(stationData['stationid'])+1): # OBS: Have to add one to include the largest id value station
        singleStation = stationData[stationData.stationid == i]
        if singleStation.empty:
            continue
        stationCount += 1

        avlbikes_idx = np.isfinite(singleStation['avlbikes'].values)
        rain_idx = weatherData['rain_MA'].values != 0 & np.isfinite(singleStation['avlbikes'].values)

        if not max(avlbikes_idx): # this checks if avlbikes_idx is all Falses
            predictors[i] = BikeAvailabilityPredictor([0], [0], [0], 0)
        else:
            # fitting polynomials to each input dataset in relation to the station-wise bike availability
            try:
                p_coeffsTemp = np.polyfit(weatherData['temperature_c'].values[avlbikes_idx], singleStation['avlbikes'].values[avlbikes_idx], 4)
            except:
                print(str(i) + " temp")
                p_coeffsTemp = [np.mean(singleStation['avlbikes'].values[avlbikes_idx])]
            try:
                p_coeffsRain = np.polyfit(weatherData['rain_MA'].values[rain_idx], singleStation['avlbikes'].values[rain_idx], 2)
            except:
                print(str(i) + " rain")
                p_coeffsRain = [np.mean(singleStation['avlbikes'].values[avlbikes_idx])]
            try:
                p_coeffsHours = np.polyfit(weatherData['Time'].values[avlbikes_idx], singleStation['avlbikes'].values[avlbikes_idx], 7) # formerly 3rd degree
            except:
                print(str(i) + " hour")
                p_coeffsHours = [np.mean(singleStation['avlbikes'].values[avlbikes_idx])]
            predictors[i] = BikeAvailabilityPredictor(p_coeffsTemp, p_coeffsRain, p_coeffsHours, max(singleStation['avlbikes'].values[avlbikes_idx]))


    return predictors, weatherData, stationData
    # end of readStationDataAndTrainPredictors()

# Run with python for example usage, otherwise include this file to use predictors as you wish
def main():
    # Now using everything that was defined previously...
    preds, weatherData, stationData = readStationDataAndTrainPredictors()

    nRows = len(weatherData)
    y_hat = np.zeros(nRows)
    y = np.zeros(nRows)

    # Analysis of R^2 by summing individual predictors and observations
    for stationID, pred in preds.items():
        stationVals = stationData[stationData.stationid == stationID]['avlbikes'].values
        for i in range(nRows):
            actual_avl = stationVals[i]
            predicted_avl = 0
            if np.isnan(actual_avl):
                actual_avl = 0
            else:
                predicted_avl = pred.predict(weatherData['temperature_c'].values[i], weatherData['rain_MA'].values[i], weatherData['Time'].values[i])
            if np.isnan(predicted_avl):
                print(str(stationID) + " " + str(i)) # This should not print, there are problems if it does
            y_hat[i] += predicted_avl
            y[i] += actual_avl




    #print(y_hat)

    corr = np.corrcoef(y_hat, y)
    coeff_determination = corr[0][1]**2
    print('Coefficient of determination (R^2) for the sum of station-wise predictions:', coeff_determination)



if __name__ == "__main__":
    main()
