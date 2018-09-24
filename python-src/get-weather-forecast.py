import sys, os
#import urllib
from xml.etree import ElementTree as ET
import urllib.request
import datetime

sys.path.append(os.path.realpath('..'))

WEATHERLOCATION = 'kaisaniemi,helsinki'
FMIAPIKEYSOURCE = 'env'
#WEATHERFORECASTOUTXMLFILE = '/prediction/weather' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.xml'
WEATHERFORECASTOUTXMLFILE = 'prediction/weatherforecast.xml'

def getFmiApiKey(f):
    root = ET.parse(f).getroot()
    return root.find('fmi-api-key').text

requestURL = 'http://data.fmi.fi/fmi-apikey/' \
           + getFmiApiKey(FMIAPIKEYSOURCE) + '/' \
           + 'wfs?request=getFeature&storedquery_id=' \
           + 'fmi::forecast::harmonie::surface::point::timevaluepair' \
           + '&place=' + WEATHERLOCATION 

req = urllib.request.Request(requestURL)
response = urllib.request.urlopen(req)
tree = ET.parse(response)
root = tree.getroot()

# Up to here OK. But parsing the wanted parts not working yet.

# This doesn't work
#temperatureElement = root.find('.//MeasurementTimeseries[@id="{http://www.opengis.net/gml/3.2}mts-1-1-Temperature"]')

print(ET.tostring(root, encoding='utf8').decode('utf8'))

#temperatureSeries = {}
#rainAmountSeries = {}
print('Individual elements: ')
temperatureElements = root.findall('.//{http://www.opengis.net/waterml/2.0}MeasurementTimeseries')
for el in temperatureElements:
    if (el.attrib['{http://www.opengis.net/gml/3.2}id'] == 'mts-1-1-Temperature'):
        temperatureSeries = el
        #print(ET.tostring(el, encoding='utf8').decode('utf8'))
    elif (el.attrib['{http://www.opengis.net/gml/3.2}id'] == 'mts-1-1-PrecipitationAmount'):
        rainAmountSeries = el
        #print(ET.tostring(el, encoding='utf8').decode('utf8'))


# This parses all MeasurementTimeseries, but I have been unable to filter the correct series by e.g. '{http://www.opengis.net/gml/3.2}id'] == 'mts-1-1-Temperature'
def parser(item1,item2):
    return item1.text,item2.text

def parse_one_series(series):
    return [parser(item1,item2) for item1,item2 in \
        zip(series.iter(tag='{http://www.opengis.net/waterml/2.0}time'), \
            series.iter(tag='{http://www.opengis.net/waterml/2.0}value'))]
    

temperatureData = zip(*(parse_one_series(temperatureSeries)))
print(list(temperatureData))

rainAmountData = zip(*(parse_one_series(rainAmountSeries)))
print(list(rainAmountData))

#temperatureElement.write(WEATHERFORECASTOUTXMLFILE)
#root.write(WEATHERFORECASTOUTXMLFILE)
