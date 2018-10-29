## Some initial thoughts on variables in the early stage of the project:

#### On independent variable 'rainintensity_mmh':

If we plot the independent variable 'rainIntensity_mmh' as such, we notice that when there's no rain, the availabilities vary between the stations, but if there's even small amount of raining, the availability-rate goes high. That consists basically from two factors: 1) people watch weather-forecasts and also observe the situation in a way that if there's been raining for the past hour, it is likely that there will be more rain (people plan whether they bike at all based on current/oncoming weather). 2) If it starts to rain while people are biking, it is also likely that they would just take the bike to the nearest stop and get bus/metro to avoid raining. We could ask for example, that would splitting the prediction calculation based on recent rains provide a better prediction than a simple linear combination of temp, rain and hour estimates?

Let's take a look the situation where we would fit a line to this data (Bike-availability vs. rainintensity_mmh):

<img src="/images/Rainintensity_mmhWithZeroValuesIncluded.png">

Fitting the line or curve to this kind of data would be problematic, so first of all we should remove the zero-raining values, because they create some skewness. Secondly, we should take into account the phenomena that people plan according to the weather forcasts. We could for example observe the history from the past 6 hours and calculate the moving average of those hours (https://en.wikipedia.org/wiki/Moving_average)

#### On independent variable 'temperature_c':

If we plot the first variable 'temperature_c', we notice that it has ideal (ideal considering the model that we apply), swarm type of distribution when plotting against our dependent 'y' variable 'sumofhourlyavg' (Bike-availability):

<img src="/images/Scatterplot_temperature_c_and_sumofhourlyavg.png">

#### Applying the polyfit for the 'temperature_c':

If we apply the 4th degree polynomial to our 'temperature_c' independent variable, we can see that it gives visually more flexible fitting curve than the basic 1st degree linear regression line. We notice that it predicts more availability, the colder it gets from +5 celcius and also more availability (according this data) when it gets over +23 - +24 celcius. If we go below 3 celcius or above 25 celcius, we would have to extrapolate instead of interpolating. Look at the end-tails below 5 celcius and 25 celcius: the inflection point is intuitively correct, if it's far too cold or hot then the bike-availability would trend upwards.

<img src="/images/Scatterplot_temperature_c_and_sumofhourlyavg_linearVSpolynomial.png">

#### The problem with the independent variable 'weekday':

We can take a look of the 'weekday' variable by plotting it like the previous ones (with bike-availability variable sumofhourlyavg). However, it does not produce that kind of nice swarm-type of scatterplot (which usually implies that that type of data is suitable for linear/polynomial models). Instead, the values are discrete, with values 0 to 6 (monday to sunday). Instead:

<img src="/images/Scatterplot_weekday_and_sumofhourlyavg.png">

As we can see from the scatterplot, weekday variable is at the end of the day a categorical variable, so it cannot be applied to our model without modifying the model to be some kind of mixed model that combines polynomial model and logistic regression model. Also, we have to think what *additional value this data would provide to our model* and just by looking it with thhis plot, there's merely any difference between the availabilitys of most of the days: we can see slightly more useage on wednesday and friday, but because it's categorical, it can be applied to logistic models, rather than linear/polynomial.

We are not applying neural networks or mathematical optimization of the coefficients applied to the n-degree polynomial predictors, so adding the variance explained by the weekday provides more complications than benefits, since the variance it can explain is only +/-30 bikes.

