#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import sys
import csv

def main(directory, inputFilename, outputFilename):
    print('Opening local file:', inputFilename)

    dateStr = convertDateformat(inputFilename[9:])
    stations = openJSON(directory + inputFilename)

    if (stations == None):
        print('file skipped')
        return None

    try:
        stations = stations['result']
        writeToCSV(outputFilename, stations, dateStr)
    except:
        print('JSON corrupted, skipping..')

def writeToCSV(outputFilename, stations, dateStr):
    print('writing to file:', outputFilename)
    with open(outputFilename, 'a', newline='') as csvfile:
        cvsWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for station in stations:
            cvsWriter.writerow([station['name'][:3], dateStr, station['avl_bikes']])

def openJSON(filename):
    # open local JSON and return json dict
    try:
        file = open(filename, 'r')
        jsonstring = file.read()
        jsonfile = json.loads(jsonstring)

        return jsonfile
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print('Error in opening file!')
        return None

def convertDateformat(t):
    # example: "20170611T005701Z" -> "2006-01-08 10:07:52"
    return t[0:4] + "-" + t[4:6] + "-" + t[6:8] + " " + t[9:11] + ":" + t[11:13] + ":" + t[13:15]