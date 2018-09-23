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
#temperatureElement = root.find('.//MeasurementTimeseries[@id="mts-1-1-Temperature"]')
#print(temperatureElement)

# This parses all MeasurementTimeseries, but I have been unable to filter the correct series by e.g. '{http://www.opengis.net/gml/3.2}id'] == 'mts-1-1-Temperature'
def parser(item1,item2):
    return item1.text,item2.text

def parse_one_series(series):
    #print('Series attributes: ', series.attrib)
    #if (series.attrib['{http://www.opengis.net/gml/3.2}id'] == 'mts-1-1-Temperature'):
    return [parser(item1,item2) for item1,item2 in \
        zip(series.iter(tag='{http://www.opengis.net/waterml/2.0}time'), \
            series.iter(tag='{http://www.opengis.net/waterml/2.0}value'))]
    

data = zip(*(parse_one_series(series) for series in tree.iter(tag='{http://www.opengis.net/waterml/2.0}MeasurementTimeseries')))

#data = zip(*(parse_one_series(series) for series in tree.findall('{http://www.opengis.net/gml/3.2}mts-1-1-Temperature')))
#data = (*(parse_one_series(series) for series in tree.iter(tag='{http://www.opengis.net/waterml/2.0}MeasurementTimeseries')))

print(list(data))
#temperatureElement.write(WEATHERFORECASTOUTXMLFILE)
#root.write(WEATHERFORECASTOUTXMLFILE)
