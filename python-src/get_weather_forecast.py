import numpy as np
import pandas as pd
import sys, os
from xml.etree import ElementTree as ET
import urllib
import socket
import datetime
from dotenv import load_dotenv, find_dotenv
from enum import Enum

def getFmiApiKey():
    load_dotenv(find_dotenv())
    return os.getenv("FMI_API_KEY")

class WeatherDataType(Enum):
    FORECAST = 'forecast'
    OBSERVATIONS = 'observations'

WEATHERLOCATION = 'kaisaniemi,helsinki'
TIMESTEP = '60'
WEATHERFORECASTOUTFILE = 'prediction/weatherforecast-HelsinkiKaisaniemi-' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.csv'
CURRENTWEATHERFORECASTFILE = 'prediction/weatherforecast-HelsinkiKaisaniemi-current.csv'
WEATHEROBSERVATIONSOUTFILE = 'prediction/weatherobservations-HelsinkiKaisaniemi-' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.csv'
CURRENTWEATHEROBSERVATIONSFILE = 'prediction/weatherobservations-HelsinkiKaisaniemi-current.csv'
REQUESTURL_FORECAST = 'http://data.fmi.fi/fmi-apikey/' \
           + str(getFmiApiKey()) + '/' \
           + 'wfs?request=getFeature&storedquery_id=' \
           + 'fmi::forecast::harmonie::surface::point::timevaluepair' \
           + '&place=' + WEATHERLOCATION

REQUESTURL_OBSERVATIONS = 'http://data.fmi.fi/fmi-apikey/' \
           + str(getFmiApiKey()) + '/' \
           + 'wfs?request=getFeature&storedquery_id=' \
           + 'fmi::observations::weather::timevaluepair' \
           + '&place=' + WEATHERLOCATION \
           + '&timestep=' + TIMESTEP + '&'

# Helper functions
def parser(item1,item2):
    return item1.text,item2.text

def parse_one_series(series):
    return [parser(item1,item2) for item1,item2 in \
        zip(series.iter(tag='{http://www.opengis.net/waterml/2.0}time'), \
            series.iter(tag='{http://www.opengis.net/waterml/2.0}value'))]

def fetchAndWriteWeatherData(weatherDataType):
    """Fetch weather data for Helsinki Kaisaniemi from FMI API.
    Write the data in the folder /prediction in a timestamp-named file.
    Takes parameter 'forecast' or 'observations'
    """
    if (weatherDataType == WeatherDataType.FORECAST):
        temp_attrib = 'mts-1-1-Temperature'
        rain_attrib = 'mts-1-1-PrecipitationAmount'
        outfile_timestamp = WEATHERFORECASTOUTFILE
        outfile_current = CURRENTWEATHERFORECASTFILE
        request_url = REQUESTURL_FORECAST
    elif (weatherDataType == WeatherDataType.OBSERVATIONS):
        temp_attrib = 'obs-obs-1-1-t2m'
        rain_attrib = 'obs-obs-1-1-r_1h'
        outfile_timestamp = WEATHEROBSERVATIONSOUTFILE
        outfile_current = CURRENTWEATHEROBSERVATIONSFILE
        request_url = REQUESTURL_OBSERVATIONS
    else:
        raise TypeError('Parameter weatherDataType must be an instance of WeatherDataType Enum')

    print('\nFetching latest weather data of type' + str(weatherDataType) +' from FMI API...')
    print('Req URL: ', request_url)
    req = urllib.request.Request(request_url)
    
    try:
        response = urllib.request.urlopen(req, timeout=10)
        parseAndWriteWeatherData(response, temp_attrib, rain_attrib, outfile_timestamp, outfile_current)
        return True
    except socket.timeout:
        print('Latest weather data could not be fetched, using old data.')
        print('socket timed out - URL %s', req)
        return False
    except urllib.error.URLError as e:
        print('Latest weather data could not be fetched, using old data.')
        """ if isinstance(e.reason, socket.timeout):
            print('  Socket timed out - URL %s', req) """
        if hasattr(e, 'reason'):
            print('  Program failed to reach FMI server.')
            print('  Reason: ', e.reason)
            
        elif hasattr(e, 'code'):
            print('Latest weather data could not be fetched, using old data.')
            print('  The FMI server couldn\'t fulfill the request.')
            print('  Error code: ', e.code)
            
        return False
   
def parseAndWriteWeatherData(response, temp_attrib, rain_attrib, outfile_timestamp, outfile_current):
    """Submethod of fetchAndWriteWeatherData."""
    tree = ET.parse(response)
    root = tree.getroot()

    measurementElements = root.findall('.//{http://www.opengis.net/waterml/2.0}MeasurementTimeseries')
    for el in measurementElements:
        if (el.attrib['{http://www.opengis.net/gml/3.2}id'] == temp_attrib):
            temperatureSeries = el
        elif (el.attrib['{http://www.opengis.net/gml/3.2}id'] == rain_attrib):
            rainAmountSeries = el

    temperatureData = zip(*(parse_one_series(temperatureSeries)))
    temperatureDataList = list(list(temperatureData))

    rainAmountData = zip(*(parse_one_series(rainAmountSeries)))
    rainDataList = list(list(rainAmountData))

    # Put the data into pandas a dataframe
    df_temperature = pd.DataFrame(temperatureDataList).T
    df_weatherData = pd.DataFrame(rainDataList).T

    df_weatherData[2] = df_temperature[1]
    df_weatherData.columns = ['Time','RainAmountPred','TemperaturePred']

    # Write to csv, both timestamped version and replace current
    # Disabled: write forecast to a timestamped file. Uncomment next line to enable.
    #df_weatherData.to_csv(outfile_timestamp, index=False)
    df_weatherData.to_csv(outfile_current, index=False)
    print('Latest weather data fetched.')

if __name__ == "__main__":
    # Execute the fetcher-writer method for both forecast and observations
    fetchAndWriteWeatherData(WeatherDataType.FORECAST)
    fetchAndWriteWeatherData(WeatherDataType.OBSERVATIONS)
