select
	station,
	hour_of_day,
	ROUND(AVG(avg),2) as avg_avg,
	ROUND(AVG(delta),2) as avg_delta
from (
	select 
		station,
		local_hour,
		avg,
		avg - lag(avg) over (order by station, local_hour) as delta,
		EXTRACT(DOW from local_hour) AS day_of_week,
		EXTRACT(HOUR from local_hour) AS hour_of_day
	from 
		hourly_avg
	order by
		station, hour_of_day, day_of_week) as data
where
	day_of_week in (0, 1, 2, 3, 4)
group by
	hour_of_day, station
order by
	station,
	hour_of_day;