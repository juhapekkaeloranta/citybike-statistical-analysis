# Data wrangling

## Step 1: Convert bike data json to csv

Availabilitydata from the citybikes is available from http://dev.hsl.fi/tmp/citybikes/. There is a json file for roughly every minute from the operation of the city bike system. That is aroung 43000 json files per month.

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

## Step 2: Aggregate

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

## Step 3: Combine weather data

TODO