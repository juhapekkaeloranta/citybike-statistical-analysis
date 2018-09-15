CREATE MATERIALIZED VIEW hourly_avg AS
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

CREATE INDEX hourly_avg_station
	ON hourly_avg (station);
	
CREATE INDEX hourly_avg_hour
	ON hourly_avg (UTC_hour);