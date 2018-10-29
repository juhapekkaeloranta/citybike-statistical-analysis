# Backend API

The server currently serves 24 hour availability prediction data in JSON format at http://localhost:3001 (local mode) and https://citybike-helsinki-predictor.herokuapp.com (Heroku deployment) with the following (REST-type) paths:

### Predictions

| Endpoint | Info | Example |
|----------|------|-------|
| `/prediction` | Predictions for all stations for next 24 h | [GET](https://citybike-helsinki-predictor.herokuapp.com/prediction/2) |
| `/prediction/$(station_id)` | Same as `prediction` but for one station | [GET](https://citybike-helsinki-predictor.herokuapp.com/prediction/2) |
| `/prediction/$(station_id)/$(timestamp)` | Same as `prediction/2` but for only one timestamp | [GET](https://citybike-helsinki-predictor.herokuapp.com/prediction/2/2018-10-08T19:00:00Z) |

Additional notes:
- `/prediction/$(station_id)/$(timestamp)`
  - The time has to be within the next 24 hours, otherwise the returned data will be empty

### Combined

The combined data range is from 12 hours before the called time to 12 hours after the called time. Actual availability data is given for the 12 hours before the called time (and is null for the 12 hours after). Prediction data covers the whole 24 hour period.

| Endpoint | Info | Example |
|----------|------|-------|
| `/combined/$(station_id)` | Prediction and actual availability for +-12 hours | [GET](https://citybike-helsinki-predictor.herokuapp.com/combined/8/) |
| `/combined/$(station_id)/$(timestamp)` | Same as `/combined/$(station_id)` but for only one timestamp | [GET](https://citybike-helsinki-predictor.herokuapp.com/combined/8/2018-09-12T12:00:00Z) |

Additional notes:
- `/combined/$(station_id)/$(timestamp)`
  - The time has to be within the next 24 hours, otherwise the returned data will be empty

## Samples 

Sample from `/combined/$(station_id)/$(timestamp)` -endpoint:

```
[
  {
    "stationid": "2",
    "time": "2018-10-29T03:00:00Z",
    "avlBikes": 1.0,
    "prediction": 10.26
  },
  {
    "stationid": "2",
    "time": "2018-10-29T04:00:00Z",
    "avlBikes": 1.0,
    "prediction": 10.2
  },
  {
    "stationid": "2",
    "time": "2018-10-29T05:00:00Z",
    "avlBikes": 3.0,
    "prediction": 10.18
  },
  {
    "stationid": "2",
    "time": "2018-10-29T06:00:00Z",
    "avlBikes": 2.0,
    "prediction": 10.04
  },
  {
    "stationid": "2",
    "time": "2018-10-29T07:00:00Z",
    "avlBikes": 8.0,
    "prediction": 9.67
  },
  {
    "stationid": "2",
    "time": "2018-10-29T08:00:00Z",
    "avlBikes": 8.0,
    "prediction": 6.58
  },
  {
    "stationid": "2",
    "time": "2018-10-29T09:00:00Z",
    "avlBikes": 8.0,
    "prediction": 6.69
  },
  {
    "stationid": "2",
    "time": "2018-10-29T10:00:00Z",
    "avlBikes": 8.0,
    "prediction": 6.66
  },
  {
    "stationid": "2",
    "time": "2018-10-29T11:00:00Z",
    "avlBikes": 5.0,
    "prediction": 6.47
  },
  {
    "stationid": "2",
    "time": "2018-10-29T12:00:00Z",
    "avlBikes": 5.0,
    "prediction": 6.42
  },
  {
    "stationid": "2",
    "time": "2018-10-29T13:00:00Z",
    "avlBikes": 5.0,
    "prediction": 6.25
  },
  {
    "stationid": "2",
    "time": "2018-10-29T14:00:00Z",
    "avlBikes": 3.0,
    "prediction": 6.35
  },
  {
    "stationid": "2",
    "time": "2018-10-29T15:00:00Z",
    "avlBikes": null,
    "prediction": 6.63
  },
  {
    "stationid": "2",
    "time": "2018-10-29T16:00:00Z",
    "avlBikes": null,
    "prediction": 6.74
  },
  {
    "stationid": "2",
    "time": "2018-10-29T17:00:00Z",
    "avlBikes": null,
    "prediction": 6.87
  },
  {
    "stationid": "2",
    "time": "2018-10-29T18:00:00Z",
    "avlBikes": null,
    "prediction": 7.0
  },
  {
    "stationid": "2",
    "time": "2018-10-29T19:00:00Z",
    "avlBikes": null,
    "prediction": 7.12
  },
  {
    "stationid": "2",
    "time": "2018-10-29T20:00:00Z",
    "avlBikes": null,
    "prediction": 7.2
  },
  {
    "stationid": "2",
    "time": "2018-10-29T21:00:00Z",
    "avlBikes": null,
    "prediction": 7.21
  },
  {
    "stationid": "2",
    "time": "2018-10-29T22:00:00Z",
    "avlBikes": null,
    "prediction": 7.13
  },
  {
    "stationid": "2",
    "time": "2018-10-29T23:00:00Z",
    "avlBikes": null,
    "prediction": 6.92
  },
  {
    "stationid": "2",
    "time": "2018-10-30T00:00:00Z",
    "avlBikes": null,
    "prediction": 6.74
  },
  {
    "stationid": "2",
    "time": "2018-10-30T01:00:00Z",
    "avlBikes": null,
    "prediction": 6.68
  },
  {
    "stationid": "2",
    "time": "2018-10-30T02:00:00Z",
    "avlBikes": null,
    "prediction": 6.74
  },
  {
    "stationid": "2",
    "time": "2018-10-30T03:00:00Z",
    "avlBikes": null,
    "prediction": 6.84
  }
]
```

