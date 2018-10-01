import numpy as np
import pandas as pd
import sys, os
from xml.etree import ElementTree as ET
import urllib.request
import datetime

sys.path.append(os.path.realpath('..'))

AVAILABILITYFOLDER = 'prediction'
# Must define how to select the latest from the folder
REQUESTURL = 'https://dev.hsl.fi/citybike/stations/' 

def fetchAndWriteCurrentAvailability():
    """Fetch the current citybike availability from HSL API.
    Write the forecast in the folder /prediction. Not implemented yet.
    Currently using dummy current availability.
    """
    return None
    
    """ req = urllib.request.Request(REQUESTURL)
    response = urllib.request.urlopen(req)

    # Write to csv
    df_weatherPred.to_csv(WEATHERFORECASTOUTCSVFILE, index=False) """
