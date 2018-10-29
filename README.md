_I wonder if there are any citybikes left on Yliopistonkatu.._ 💭

# Citybike predictor

[Citybike predictor](https://citybike-pred.herokuapp.com/) shows the past and predicted availability of citybikes! 

<img width="75%" src="/images/application_screencapture.png">

These examples demonstrate the usefulness predictions in various situations:

<img src="/images/example_situations.png">

1. No bikes but availability is likely to increase - wait a while and get a bike  🚲
2. There are some bikes but not for long - hurry up!  🏃
3. No bikes and no spikes for a while - take the bus  🚎

### Application

- The application is available at [https://citybike-pred.herokuapp.com/](https://citybike-pred.herokuapp.com/). 
- The predictions are provided from a REST API at [https://citybike-helsinki-predictor.herokuapp.com/](https://citybike-helsinki-predictor.herokuapp.com/). 

> Please note that our current application servers might take around 30-45 seconds the start if they have gone idle.

**Winter is coming!**
- Application will go to demo-mode during off-season _(31.10.2018 - next spring)_

# Technical

## Data

We have combined citybike availability data from HSL and weather data from FMI. Read more about the data here: ["Data wrangling and backend operation"](/docs/data-wrangling.md)

### Data sources
* Bike availability:
  * City bike data source (both historical download and online): https://dev.hsl.fi/citybike/stations/
* Weather data: Ilmatieteen laitos / Finnish Meteorological Institute under license CC BY 4.0.
  * Historical data loaded from: https://ilmatieteenlaitos.fi/havaintojen-lataus#!/
  * Weather observations and predictions loaded from FMI open data API, see https://en.ilmatieteenlaitos.fi/open-data-manual-fmi-wfs-services

### Historical data available
For testing and demonstration purposes we have prepared data from 7 months (2017-06, 2017-08, 2017-09, 2018-06, 2018-07, 2018-08 and 2018-09). Please see the `/data`-folder for more details.

## Source code

- [Backend](python-src/server.py) source code is in this repository
- [Frontend](https://github.com/mikkokotola/citybike-front/) for the citybike predictor app is a separate repository. 

## Model

The model is a "mixed model" consisting of a linear combination of different n-degree polynomials that were fit for each factor in relation to station bike-availability (factors: temperature, rain amount, hour of the day). The model is trained on data from 2018-08 and 2018-09. The R^2 value of the model (0.563288572018) provides a basic measure of how well the observed outcomes of bike-availability are predicted by our model. Notice: the observations for the bike-availability as a single data-series was obtained by summing the bike-availability data-series for each bike-station. We call this the "aggregate availability". Likewise, the prediction data-series was obtained by summing the bike-availability predictions for each bike station. 

Read more about the model here: ["Model"](/docs/model.md)

Was the choice of predictors chrystal clear from the start? Nope. Read some thoughts on model variables in the early stage of the project: ["Early thoughts on variables"](/docs/early-thoughts.md)

## Backend server API

Backend server has REST API has endpoints predictions and past availability. For more detailed information please see: [API docs](/docs/api.md)

# About

The service was a project for "Introduction to Data Science" -course at the University of Helsinki Data Science master's programme, fall 2018.

### Contributors
* Lea Kosonen (focus: machine learning model)
* Mikko Kotola (focus: backend and weather data)
* Juha-Pekka Moilanen (focus: frontend and bike data)

### Roadmap

How could the project be continued? See [roadmap](/docs/roadmap.md).

---

# Development

### Server

To start backend server, run: 

```
python python-src/server.py
```

Server will start on `localhost:3001`.

The server expects the environment variable FMI_API_KEY to be found in either in actual environment variables or the file .env located at the root of the project. Contents of the .env file:
```
FMI_API_KEY=your-fmi-apikey-here
```

For e.g. Heroku deployment, you can set the environment variable with the command:
```
heroku config:set FMI_API_KEY=your-fmi-apikey-here
```

### Frontend

NOTE: frontend is in a different repository: [Citybike-front](https://github.com/mikkokotola/citybike-front).

1. Go to frontend repository root and start a local webserver to serve html and js files

```
python3 -m http.server
```

2. Open browser from localhost:8000
3. Click on home.html

NOTE: the frontend uses the Heroku-deployed backend. If you want to use a locally run backend, change the first line in js-src/plotter.js to const baseUrl = 'http://localhost:3001'

<img src="/images/Citybikes_Arabia_2018_10_17.jpg" alt="Citybikes at Arabia, Helsinki; photo: Mikko Kotola">
