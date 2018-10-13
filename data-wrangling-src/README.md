## Convert bike data json to csv

City bike data available from http://dev.hsl.fi/tmp/citybikes/. There is a json file for roughly every minute from the operation of the city bike system.

Sample:

```json
{
  result: [
    {
      name: "001 Kaivopuisto",
      coordinates: "60.155411,24.950391",
      total_slots: 30,
      free_slots: 6,
      avl_bikes: 29,
      operative: true,
      style: "Station on"
    },
    {
      name: "002 Laivasillankatu",
      coordinates: "60.159715,24.955212",
      total_slots: 12,
      free_slots: 9,
      avl_bikes: 2,
      operative: true,
      style: "Station on"
    },
```

The files contain a lot of repeated information. This script extracts the availability data from the json's to a csv file.

Output sample:

```
001,2017-06-01 05:34:01,5
002,2017-06-01 05:34:01,0
003,2017-06-01 05:34:01,1
004,2017-06-01 05:34:01,0
005,2017-06-01 05:34:01,2
006,2017-06-01 05:34:01,12
007,2017-06-01 05:34:01,0
008,2017-06-01 05:34:01,8
009,2017-06-01 05:34:01,19
010,2017-06-01 05:34:01,9
011,2017-06-01 05:34:01,12
012,2017-06-01 05:34:01,9
013,2017-06-01 05:34:01,6
014,2017-06-01 05:34:01,12
015,2017-06-01 05:34:01,13
```

### Usage

1. Place json's in a directory, example: 'stations-2017-06'
2. Run `python3 processFiles.py`
3. Script will prompt for directory and output filename
4. Wait for script to process
5. Add headers manually to csv file if needed