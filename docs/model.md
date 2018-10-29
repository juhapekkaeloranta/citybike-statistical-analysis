## Model

The model is a "mixed model" consisting of a linear combination of different n-degree polynomials that were fit for each factor in relation to station bike-availability (factors: temperature, rain amount, hour of the day). 

We can look at the three scatterplots that represent each factors' relationship with the bike availability on the aggregate level:

Bike-availability vs. temperature:

<img src="/images/ScatterplotRelationshipBetweenAvailabilityAndTemperature.png">

Bike-availability vs. hour of the day:

<img src="/images/ScatterplotRelationshipBetweenAvailabilityAndHourOfTheDay.png">

Bike-availability vs. rain amount (precipitation):

<img src="/images/ScatterplotRelationshipBetweenAvailabilityAndRain.png">

We assume that each station has its own trend with each of the factors and the station's bike-availability, so that is how the factors are utilized at the station-level to fit n-degree polynomials for station-wise prediction purposes.

The model is trained on data from 2018-08 and 2018-09. The R^2 value of the model (0.563288572018) provides a basic measure of how well the observed outcomes of bike-availability are predicted by our model. Notice: the observations for the bike-availability as a single data-series was obtained by summing the bike-availability data-series for each bike-station. We call this the "aggregate availability". Likewise, the prediction data-series was obtained by summing the bike-availability predictions for each bike station. 

The R^2 value of the model was obtained by training and verifying the model based on the months 2018-08 and 2018-09. R^2, also known as the coefficient of determination, is a statistical measure that tells how similar two data series are: in this case, the predictions vs. the observations for bike availability. We can look this visually by plotting the predicted availability (red line) and observed (actual) aggregate-availability (blue line) by time that includes months 2018-08 and 2018-09:

<img src="/images/TwoMonthsActualvsPredictedAggregateAvailability.png">
