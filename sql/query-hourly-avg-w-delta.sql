select 
	station,
	local_hour,
	avg,
	avg - lag(avg) over (order by station, local_hour) as delta,
	EXTRACT(DOW from local_hour) AS day_of_week,
	EXTRACT(HOUR from local_hour) AS hour_of_day,
	EXTRACT(YEAR from local_hour) AS year,
	EXTRACT(MONTH from local_hour) AS month_of_year,
	EXTRACT(DAY from local_hour) AS day_of_month 
from 
	hourly_avg
order by
	station,
	local_hour;