# Statistical analysis of citybike availability in Helsinki

Project for "Introduction to Data Science" -course

### City bike data
* Original city bike data source: https://dev.hsl.fi/citybike/stations/

### Weather data
* Weather data source: Ilmatieteen laitos / Finnish Meteorological Institute under licence CC BY 4.0.
* Historical data loaded from: https://ilmatieteenlaitos.fi/havaintojen-lataus#!/

### Population data
* Population data source: Statistics Finland
* Population data loaded from: http://pxnet2.stat.fi/PXWeb/pxweb/en/Postinumeroalueittainen_avoin_tieto/Postinumeroalueittainen_avoin_tieto__2018/paavo_9_koko_2018.px/

### Coordinate conversion
Population data includes data by postal code area. Postal code area location is given in ETRS89-TM35FIN (Finnish coordinate system). Coordinates can be converted to latitude and longitued (in WGS84 or EUREF-FIN) using e.g. http://coordtrans.fgi.fi/transform.jsp or http://loukko.net/koord_proj/. Note: check which lat-lon system the citybike data and weather data lat-lon coordinates are in.

### Other resources
* Some r-scripts: https://github.com/juhapekkamoilanen/citybike-data-analysis
* Some visualizations: https://github.com/citybike-statistics/citybike-statistics.github.io
