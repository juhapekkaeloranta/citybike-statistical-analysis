import numpy as np
import pandas as pd
import sys, os
import urllib.request
import socket
import datetime
import json
import constants
import conversion
import re

PASTAVAILABILITYOUTFILE = 'prediction/pastavailabilities-' + datetime.datetime.now().replace(microsecond=0).isoformat() + '.csv'
CURRENTPASTAVAILABILITYFILE = 'prediction/pastavailabilities-current.csv'
BASEURL = 'https://dev.hsl.fi/citybike/stations/' 

def fetchAndWriteCurrentAvailability():
    """Fetch the citybike availability from HSL API for the last 12 hours.
    Note: the availabilities are the spot availabilities at the even hours.
    Write the availabilities in the folder /prediction.
    """
    timeNowAsDateTime = datetime.datetime.utcnow().replace(microsecond=0)
    timeNow = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    timeStr = formatTimeStringToHSL(timeNow)

    times = []
    timeStrs = []
    for x in range(13):
        times.append((timeNowAsDateTime - datetime.timedelta(hours=x)).isoformat())
        timeStrs.append(formatTimeStringToHSL(times[x]))

    df = fetchSeriesOfFiles(timeStrs)
    df['time'] = df['time'].apply(lambda t: conversion.getUTCTimeStampFromTimeStampString(str(t)))
    
    # Write to csv
    # Disabled: write out timestamped past availability file. Uncomment next line to enable.
    #df.to_csv(PASTAVAILABILITYOUTFILE, index=False)
    df.to_csv(CURRENTPASTAVAILABILITYFILE, index=False)

def formatTimeStringToHSL(time):
    timeStr = str(time)
    timeStr = timeStr.translate({ord(c): None for c in '-:'})
    timeStr = timeStr[:11] + '0001Z'
    return timeStr

def formatTimeStringToData(timeStr):
    timeStr = timeStr[:11] + '0000Z'
    time = datetime.datetime.strptime(timeStr, "%Y%m%dT%H%M%SZ")
    return time

def parseAndWriteWeatherForecast(response):
    """ 
    # Write to csv, both timestamped version and replace current
    df_weatherPred.to_csv(WEATHERFORECASTOUTFILE, index=False)
    df_weatherPred.to_csv(CURRENTWEATHERFORECASTFILE, index=False)
    print('Latest weather forecast fetched.') """

def fetchSingleFile(timeStr):
    reqURL = BASEURL + 'stations_' + timeStr + '.json'
    print('Sending request to: ', reqURL)
    req = urllib.request.Request(reqURL)
    
    try:
        response = urllib.request.urlopen(req, timeout=10)
        #parseAndWriteWeatherForecast(response)
        return json.load(response)
    except socket.timeout:
        print('Bike availability data could not be fetched.')
        print('  Socket timed out - URL %s', req)
        return False
    except urllib.error.URLError as e:
        print('Bike availability data could not be fetched.')
        
        if hasattr(e, 'reason'):
            print('  Program failed to reach HSL server.')
            print('  Reason: ', e.reason)
            
        elif hasattr(e, 'code'):
            print('Bike availability data could not be fetched.')
            print('  The HSL server couldn\'t fulfill the request.')
            print('  Error code: ', e.code)
            
        return False

def fetchSeriesOfFiles(timeStrs):
    aggregateDf = pd.DataFrame(columns=['stationid', 'time', 'avlbikes'])
    dirFileList = fetchDirectoryFileList()
    for timeStr in timeStrs:
        digits = 1
        searchResult = None
        while (digits <=4 and not searchResult):
            timeStrRegEx = regexFromTimeStr(timeStr, digits)
            searchResult = timeStrRegEx.search(dirFileList)
            digits += 1
        if not searchResult:
            continue
        fileNameMatch = searchResult.group()
        results = fetchSingleFile(fileNameMatch)
        if results:
            results = results['result']
            df = singleResultToDataframe(results, timeStr)
            aggregateDf = pd.concat([aggregateDf, df], axis=0, ignore_index=True)
    aggregateDf.sort_values(by=['time', 'stationid'], axis=0)
    return aggregateDf

def regexFromTimeStr(timeStr, digits):
    return (re.compile(timeStr[:(15-digits)] + r'\d{' + str(digits) + '}Z'))

def singleResultToDataframe(results, timeStr):
    df = pd.DataFrame(columns=['stationid', 'time', 'avlbikes'])
    i = 0

    for res in results:
        #print(res['name'].split()[0])
        stationNumber = int(res['name'].split()[0])
        timeToData = formatTimeStringToData(timeStr)
        avlbikes = res['avl_bikes']
        if (stationNumber in constants.stationIds):
            df.loc[i,'stationid'] = stationNumber
            df.loc[i,'time'] = timeToData
            df.loc[i,'avlbikes'] = avlbikes
            i += 1
    return df

def fetchDirectoryFileList():
    reqURL = BASEURL
    print('Sending request to: ', reqURL)
    req = urllib.request.Request(reqURL)
    
    try:
        response = urllib.request.urlopen(req, timeout=10)
        return(str(response.read()))
    except socket.timeout:
        print('Bike availability data index could not be fetched.')
        print('  Socket timed out - URL %s', req)
        return False
    except urllib.error.URLError as e:
        print('Bike availability data index could not be fetched.')
        
        if hasattr(e, 'reason'):
            print('  Program failed to reach HSL server.')
            print('  Reason: ', e.reason)
            
        elif hasattr(e, 'code'):
            print('Bike availability data index could not be fetched.')
            print('  The HSL server couldn\'t fulfill the request.')
            print('  Error code: ', e.code)
            
        return False

if __name__ == "__main__":
    # Execute the fetcher-writer method
    fetchAndWriteCurrentAvailability()
