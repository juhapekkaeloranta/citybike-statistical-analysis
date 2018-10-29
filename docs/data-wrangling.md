# Data wrangling and backend processing

## Step 1: Get historical bike data in JSON and convert to CSV

Availability data from the citybike stations is available from http://dev.hsl.fi/tmp/citybikes/. Currently some data is missing from HSL API but we managed to get some via email by asking nicely from the provider. There is a json file for roughly every minute from the operation of the city bike system.

That is around 43000 json files per month...

Sample:

```json
{
  "result": [
    {
      "name": "001 Kaivopuisto",
      "coordinates": "60.155411,24.950391",
      "total_slots": 30,
      "free_slots": 6,
      "avl_bikes": 29,
      "operative": true,
      "style": "Station on"
    },
    {
      "name": "002 Laivasillankatu",
      "coordinates": "60.159715,24.955212",
      "total_slots": 12,
      "free_slots": 9,
      "avl_bikes": 2,
      "operative": true,
      "style": "Station on"
    },
```

We used a python [script](/data-wrangling-src/processFiles.py) to combine these into one csv file per month.

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

## Step 2: Aggregate historical bike availability data

With around 250 stations this csv has 250*43000=11M rows. We reduced it by taking avegare for each hour. Now the rowcount is aroung 100K per month which is easier to manage. Here's the [script](/data-wrangling-src/calc-hourly-avg.py).

Sample:

```
stationid,time,avlbikes
1,2017-06-01 00:00:00,23.0
1,2017-06-01 01:00:00,23.0
1,2017-06-01 02:00:00,23.0
1,2017-06-01 03:00:00,23.0
1,2017-06-01 04:00:00,10.3
1,2017-06-01 05:00:00,5.4
1,2017-06-01 06:00:00,4.4
1,2017-06-01 07:00:00,0.8
1,2017-06-01 08:00:00,0.5
1,2017-06-01 09:00:00,0.0
1,2017-06-01 10:00:00,0.6
1,2017-06-01 11:00:00,2.8
1,2017-06-01 12:00:00,4.0
1,2017-06-01 13:00:00,12.2
```

Note: The same thing can be achieved with SQL like this:

```sql
select 
	stationid as station, 
	date_trunc('hour', time) as UTC_hour,
	round(avg(avlbikes),1) as avg
from 
	citybikeschema.availability
group by 
	station, UTC_hour
order by 
	UTC_hour, station;
```

## Step 3: Fetch bike availability for the last 12 hours
Bike availability data for the last 12 hours is fetched from the same source as the historical data: http://dev.hsl.fi/tmp/citybikes/. Because the source data is by the minute and aggregation would be somewhat heavy in runtime, the script in [get_current_availability.py]((/python-src/get_current_availability.py) reads the directory listing and picks the first available minute after every even hour. This is most often of type https://dev.hsl.fi/citybike/stations/stations_20181026T160001Z.json (the scripts writing the source data finish at one second past the hour most of the time), but sometimes the first available data is several minutes past the hour. The script then writes the availabilities for the last 12 hours into [csv](/prediction/pastavailabilities-current.csv) in similar format as the historical hourly aggregated availabilities.

## Step 4: Fetch weather observations and forecasts
Weather data is fetched from the Finnish Meteorological Institute under license CC BY 4.0.
*Historical data* was loaded in CSV format from: https://ilmatieteenlaitos.fi/havaintojen-lataus#!/

Sample / Historical weather data:

```
Vuosi,Kk,Pv,Klo,Aikavyöhyke,Sateen intensiteetti (mm/h),Ilman lämpötila (degC)
2016,4,1,00:00,UTC,0,1
2016,4,1,01:00,UTC,0,0.7
2016,4,1,02:00,UTC,0,0.6
2016,4,1,03:00,UTC,0,0.6
2016,4,1,04:00,UTC,0,0.4
2016,4,1,05:00,UTC,0,0.5
2016,4,1,06:00,UTC,0,0.8
2016,4,1,07:00,UTC,0,1.1
```

*Weather predictions* for the next 24 hours and *weather observations* for the last 12 hours are loaded in runtime from FMI open data API (see https://en.ilmatieteenlaitos.fi/open-data-manual-fmi-wfs-services). The functions are in the file [get_weather_forecast.py](/python-src/get_weather_forecast.py) Example calls to the FMI API are:

```
# Get weather forecast for Kaisaniemi, Helsinki for the next 24 h
http://data.fmi.fi/fmi-apikey/KEYHERE/wfs?request=getFeature&storedquery_id=fmi::forecast::harmonie::surface::point::timevaluepair&place=kaisaniemi,helsinki

# Get weather observations for Kaisaniemi, Helsinki for the last 12 h in 60 minute steps
http://data.fmi.fi/fmi-apikey/KEYHERE/wfs?request=getFeature&storedquery_id=fmi::observations::weather::timevaluepair&place=kaisaniemi,helsinki&timestep=60
```
The API calls provide XML that has is parsed and written into csv in similar format as the historical data.

## Step 5: Train model using historical bike availability and weather data
For model creation the historical bike availability and weather data are read from two separate csv files and converted into Pandas dataframes. The model is trained using these two dataframes.

The trained model is written into a pickle file (in /trainedModel/) to avoid having to recreate and train the model at runtime. The trained model is simply read in runtime from the pickle file into memory. This improves performance especially on Heroku, where the dynos must restart the program after being inactive.

## Step 6: Upon request, create predictions using the model and weather data for the last 12 hours
The predictions are created in runtime. The user clicks on a station and the frontend sends a station-specific request like https://citybike-helsinki-predictor.herokuapp.com/combined/2 to the backend. The backend
* Wakes up from inactive state (in Heroku) (if dyno was inactive)
* Loads predictors (model) from memory  (if dyno was inactive)
* Updates the bike availability data for the last 12 h for all stations (if data over 10 min old)
* Updates the weather observations for the last 12 h and weather prediction for the next 24 h (if data over 3 min old)
* Creates availability predictions (using the model) for the last 12 h based on the weather observations and for the next 12 h based on the weather forecast - and combines these two into a combined prediction
* Reads in the combined predictions and bike availability data and merges these into one Pandas dataframe
* Filters the data by the requested station
* For the requested station, returns the availability of the bikes in the last 12 h and the predicted availability both in the last 12 h and the next 12 h

## Other kinds of predictions supported by the backend API

See [API documentation](/docs/api.md) for more details



