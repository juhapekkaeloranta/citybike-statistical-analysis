import numpy as np
import pandas as pd
import sys, os
from xml.etree import ElementTree as ET
import urllib.request
import datetime

def getFmiApiKey(f):
    root = ET.parse(f).getroot()
    return root.find('fmi-api-key').text

WEATHERLOCATION = 'kaisaniemi,helsinki'
FMIAPIKEYSOURCE = 'env'
WEATHERFORECASTOUTFILE = 'prediction/weatherforecast-HelsinkiKaisaniemi-' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.csv'
CURRENTWEATHERFORECASTFILE = 'prediction/weatherforecast-HelsinkiKaisaniemi-current.csv'
REQUESTURL = 'http://data.fmi.fi/fmi-apikey/' \
           + getFmiApiKey(FMIAPIKEYSOURCE) + '/' \
           + 'wfs?request=getFeature&storedquery_id=' \
           + 'fmi::forecast::harmonie::surface::point::timevaluepair' \
           + '&place=' + WEATHERLOCATION


# Helper functions
def parser(item1,item2):
    return item1.text,item2.text

def parse_one_series(series):
    return [parser(item1,item2) for item1,item2 in \
        zip(series.iter(tag='{http://www.opengis.net/waterml/2.0}time'), \
            series.iter(tag='{http://www.opengis.net/waterml/2.0}value'))]

def fetchAndWriteWeatherForecast():
    """Fetch the current weather forecast for Helsinki Kaisaniemi from FMI API.
    Write the forecast in the folder /prediction in a timestamp-named file.
    """
    print('\nFetching latest weather forecast from FMI API...')
    req = urllib.request.Request(REQUESTURL)
    response = urllib.request.urlopen(req)

    # Parse the temperature and rain forecasts from the FMI XML file
    tree = ET.parse(response)
    root = tree.getroot()

    measurementElements = root.findall('.//{http://www.opengis.net/waterml/2.0}MeasurementTimeseries')
    for el in measurementElements:
        if (el.attrib['{http://www.opengis.net/gml/3.2}id'] == 'mts-1-1-Temperature'):
            temperatureSeries = el
        elif (el.attrib['{http://www.opengis.net/gml/3.2}id'] == 'mts-1-1-PrecipitationAmount'):
            rainAmountSeries = el

    temperatureData = zip(*(parse_one_series(temperatureSeries)))
    temperatureDataList = list(list(temperatureData))

    rainAmountData = zip(*(parse_one_series(rainAmountSeries)))
    rainDataList = list(list(rainAmountData))

    # Put the data into pandas a dataframe
    df_temperature = pd.DataFrame(temperatureDataList).T
    df_weatherPred = pd.DataFrame(rainDataList).T

    df_weatherPred[2] = df_temperature[1]
    df_weatherPred.columns = ['Time','RainAmountPred','TemperaturePred']

    # Write to csv, both timestamped version and replace current
    df_weatherPred.to_csv(WEATHERFORECASTOUTFILE, index=False)
    df_weatherPred.to_csv(CURRENTWEATHERFORECASTFILE, index=False)
    print('Latest weather forecast fetched.')

# Execute the fetcher-writer method
fetchAndWriteWeatherForecast()
