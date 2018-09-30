# Statistical analysis of citybike availability in Helsinki

Project for "Introduction to Data Science" -course.

### Project plan
[Project plan](https://docs.google.com/document/d/1X3f5UQMo5cpXqYQnJM6-z-aw4sNIrAeuVKdYuzaYq7E/edit?usp=sharing) (preliminary) in google docs.

### City bike data
* Original city bike data source: https://dev.hsl.fi/citybike/stations/

### Weather data
* Weather data source: Ilmatieteen laitos / Finnish Meteorological Institute under license CC BY 4.0.
* Historical data loaded from: https://ilmatieteenlaitos.fi/havaintojen-lataus#!/

### Coordinate conversion
Population data includes data by postal code area. Postal code area location is given in ETRS89-TM35FIN (Finnish coordinate system). Coordinates can be converted to latitude and longitued (in WGS84 or EUREF-FIN) using e.g. http://coordtrans.fgi.fi/transform.jsp or http://loukko.net/koord_proj/. Note: check which lat-lon system the citybike data and weather data lat-lon coordinates are in.

### Other resources
* Some r-scripts: https://github.com/juhapekkamoilanen/citybike-data-analysis
* Some visualizations: https://github.com/citybike-statistics/citybike-statistics.github.io

# Development

### Web-application

1. Start a local webserver

```
python3 -m http.server
```

2. Open browser from localhost:8000