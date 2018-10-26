# Statistical analysis of citybike availability in Helsinki

Project for "Introduction to Data Science" -course.

### Related repositories
[Frontend](https://github.com/mikkokotola/citybike-front/) for the citybike predictor app is a separate repository. This repository contains backend code.

### Deployment
Frontend is deployed at [https://citybike-pred.herokuapp.com/](https://citybike-pred.herokuapp.com/). The frontend uses the python backend deployed at [https://citybike-helsinki-predictor.herokuapp.com/](https://citybike-helsinki-predictor.herokuapp.com/).

Please note that Heroku dynos go to inactive mode for non-active apps and may take up to 30-45 seconds to wake up and run after call.

### Project plan
[Project plan](https://docs.google.com/document/d/1X3f5UQMo5cpXqYQnJM6-z-aw4sNIrAeuVKdYuzaYq7E/edit?usp=sharing) (preliminary) in google docs.

### City bike data
* City bike data source (both historical download and online): https://dev.hsl.fi/citybike/stations/

### Weather data
* Weather data source: Ilmatieteen laitos / Finnish Meteorological Institute under license CC BY 4.0.
* Historical data loaded from: https://ilmatieteenlaitos.fi/havaintojen-lataus#!/
* Weather observations and predictions loaded from FMI open data API, see https://en.ilmatieteenlaitos.fi/open-data-manual-fmi-wfs-services

### Documentation
* [Data wrangling and backend operation](/docs/data-wrangling.md)

### Other resources
* Some r-scripts: https://github.com/juhapekkamoilanen/citybike-data-analysis
* Some visualizations: https://github.com/citybike-statistics/citybike-statistics.github.io

# Details on the current model and data

## Model
The model is a "mixed model" consisting of a linear combination of different n-degree polynomials that were fit for each factor in relation to station bike-availability (factors: temperature, rain amount, hour of the day). The model is trained on data from 2018-08 and 2018-09.

## Historical data available
* Historical data includes months 2017-06, 2017-08, 2017-09, 2018-06, 2018-07, 2018-08 and 2018-09

# Backend server API

The server currently serves 24 hour availability prediction data in JSON format at http://localhost:3001 (local mode) and https://citybike-helsinki-predictor.herokuapp.com (Heroku deployment) with the following (REST-type) paths:

Predictions for all stations for 24 h :
[/prediction](https://citybike-helsinki-predictor.herokuapp.com/prediction)

Predictions for a single station defined by station id for 24 h :
[/prediction/2](https://citybike-helsinki-predictor.herokuapp.com/prediction/2) (here station id 2)

Predictions for a station defined by station id and a single hour:
[/prediction/2/2018-10-08T19:00:00Z](https://citybike-helsinki-predictor.herokuapp.com/prediction/2/2018-10-08T19:00:00Z) (here station id 2 and time Oct 8th 2018 19:00)

Combined predictions for +-12 hours:
[/combined/2](https://citybike-helsinki-predictor.herokuapp.com/combined/2) (here station id 2)

The server also serves combined historical data at paths formatted like:
[/combined/8/2018-09-12T12:00:00Z](https://citybike-helsinki-predictor.herokuapp.com/combined/8/2018-09-12T12:00:00Z) (here station id 8 and centre time Sept 12th 2018 12:00)

The combined data range is from 12 hours before the called time to 12 hours after the called time. Actual availability data is given for the 12 hours before the called time (and is null for the 12 hours after). Prediction data covers the whole 24 hour period.

# Development

### Server

To start backend server, run: 

```
python python-src/server.py
```

Server will start on `localhost:3001`

### Frontend

NOTE: frontend is in a different repository: [Citybike-front](https://github.com/mikkokotola/citybike-front).

1. Go to frontend repository root and start a local webserver to serve html and js files

```
python3 -m http.server
```

2. Open browser from localhost:8000
3. Click on home.html

NOTE: the frontend uses the Heroku-deployed backend. If you want to use a locally run backend, change the first line in js-src/plotter.js to const baseUrl = 'http://localhost:3001'

