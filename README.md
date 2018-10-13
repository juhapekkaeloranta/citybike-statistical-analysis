# Statistical analysis of citybike availability in Helsinki

Project for "Introduction to Data Science" -course.

### Project plan
[Project plan](https://docs.google.com/document/d/1X3f5UQMo5cpXqYQnJM6-z-aw4sNIrAeuVKdYuzaYq7E/edit?usp=sharing) (preliminary) in google docs.

### City bike data
* Original city bike data source: https://dev.hsl.fi/citybike/stations/

### Weather data
* Weather data source: Ilmatieteen laitos / Finnish Meteorological Institute under license CC BY 4.0.
* Historical data loaded from: https://ilmatieteenlaitos.fi/havaintojen-lataus#!/
* Weather predictions loaded from FMI open data API, see https://en.ilmatieteenlaitos.fi/open-data-manual-fmi-wfs-services

### Other resources
* Some r-scripts: https://github.com/juhapekkamoilanen/citybike-data-analysis
* Some visualizations: https://github.com/citybike-statistics/citybike-statistics.github.io

# Development

### Server

To start backend server, run: 

```
python python-src/server.py
```

Server will start on `localhost:3001`

### Frontend

1. Start a local webserver to serve html and js files

```
python3 -m http.server
```

2. Open browser from localhost:8000

## Server API

The server currently serves 24 hour availability prediction data in JSON format at http://localhost:3001 with the following (REST-type) paths:

Predictions for all stations for 24 h :
/prediction

Predictions for a single station defined by station id for 24 h :
/prediction/2 (here station id 2)

Predictions for a station defined by station id and a single hour:
/prediction/2/2018-10-08T19:00:00Z (here station id 2 and time Oct 8th 2018 19:00)

The server also serves historical data in JSON format at paths formatted like:
/combined/8/2018-09-12T12:00:00Z (here station id 8 and centre time Sept 12th 2018 12:00)

The historical data range is from 12 hours before the called time to 12 hours after the called time. Actual availability data is given for the 12 hours before the called time (and is null for the 12 hours after). Prediction data covers the whole 24 hour period.
