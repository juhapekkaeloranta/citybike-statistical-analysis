# Statistical analysis of citybike availability in Helsinki

Project for "Introduction to Data Science" -course.

### Project plan
[Project plan](https://docs.google.com/document/d/1X3f5UQMo5cpXqYQnJM6-z-aw4sNIrAeuVKdYuzaYq7E/edit?usp=sharing) (preliminary) in google docs.

### City bike data
* Original city bike data source: https://dev.hsl.fi/citybike/stations/

### Weather data
* Weather data source: Ilmatieteen laitos / Finnish Meteorological Institute under license CC BY 4.0.
* Historical data loaded from: https://ilmatieteenlaitos.fi/havaintojen-lataus#!/

### Other resources
* Some r-scripts: https://github.com/juhapekkamoilanen/citybike-data-analysis
* Some visualizations: https://github.com/citybike-statistics/citybike-statistics.github.io

# Development

### Server

To start server, run file python-src/server.py. The server currently serves 24 hour availability prediction data (all stations) in JSON format at localhost:3001/prediction.

### Web-application

1. Start a local webserver

```
python3 -m http.server
```

2. Open browser from localhost:8000
