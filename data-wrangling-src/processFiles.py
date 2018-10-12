#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import observationJSONtoCSV

directories = [f for f in os.listdir('.') if os.path.isdir(f)]

print('Choose directory:')
for i in range(len(directories)):
    print('[' + str(i) + ']: ' + str(directories[i]))

chosen = int(input('Enter number: '))
pathToFiles = "./" + str(directories[chosen]) + "/"

files = [f for f in os.listdir(pathToFiles) if os.path.isfile(pathToFiles + f)]

print('Processing directory: ' + pathToFiles)
print('Found ' + str(len(files)) + ' files.')

cmd = str(input('Continue: [Y/N] '))

if (cmd != "Y"):
    print('Aborting')
    sys.exit(0)

outputFilename = str(input('Output filename? [bikeAvailability-YYYY-MM.csv] '))

for f in files:
    if (f[:8] == 'stations'):
        print('Processing file: ' + f)        
        observationJSONtoCSV.main(pathToFiles, f, outputFilename)
        print('finished file')