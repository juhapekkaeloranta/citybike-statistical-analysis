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
import asyncio
from aiohttp import ClientSession
   
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

    fetcher = Fetcher()
    df = fetcher.fetchSeriesOfFiles(timeStrs)
    df['time'] = df['time'].apply(lambda t: conversion.getUTCTimeStampFromTimeStampString(str(t)))
    
    # Write to csv
    # Disabled: write out timestamped past availability file. Uncomment next line to enable.
    #df.to_csv(PASTAVAILABILITYOUTFILE, index=False)
    df.to_csv(CURRENTPASTAVAILABILITYFILE, index=False)
    print('Wrote current 12 h availabilities to file ', CURRENTPASTAVAILABILITYFILE)

def formatTimeStringToHSL(time):
    timeStr = str(time)
    timeStr = timeStr.translate({ord(c): None for c in '-:'})
    timeStr = timeStr[:11] + '0001Z'
    return timeStr

def formatTimeStringToData(timeStr):
    timeStr = timeStr[:11] + '0000Z'
    time = datetime.datetime.strptime(timeStr, "%Y%m%dT%H%M%SZ")
    return time

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

class Fetcher():
    async def fetch(self, url, session):
        print('Sending request to: ', url)
        async with session.get(url) as response:
            return await response.read()

    async def runParallelFetch(self, files):
        url = BASEURL + 'stations_{}.json'
        tasks = []

        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        async with ClientSession() as session:
            for f in files:
                task = asyncio.ensure_future(self.fetch(url.format(f), session))
                tasks.append(task)

            self.fetchedAvailabilities = await asyncio.gather(*tasks)
    
    def fetchSeriesOfFiles(self, timeStrs):
        dirFileList = self.fetchDirectoryFileList()
        
        addresses = self.getAvailabilityAddresses(timeStrs, dirFileList)
        
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.runParallelFetch(addresses))
        loop.run_until_complete(future)

        aggregateDf = pd.DataFrame(columns=['stationid', 'time', 'avlbikes'])
        results = self.fetchedAvailabilities
        if results:
            for index, result in enumerate(results):
                res = json.loads(result.decode('utf-8'))
                res = res['result']
                df = singleResultToDataframe(res, timeStrs[index])
                aggregateDf = pd.concat([aggregateDf, df], axis=0, ignore_index=True)

        aggregateDf.sort_values(by=['time', 'stationid'], axis=0)
        return aggregateDf

    def getAvailabilityAddresses(self, timeStrs, dirFileList):
        addresses = []
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
            addresses.append(fileNameMatch)
        return addresses

    def fetchDirectoryFileList(self):
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
