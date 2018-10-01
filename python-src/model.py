import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split

def assignModelVariables(combined):
    print('\n** Assigning variables to model **')
    print('Assign avlbikes')
    # Assign 'avlbikes' as the dependent variable y
    y = combined['avlbikes']

    print('Assign weather')
    # Assign 'rainIntensity_mmh' and 'temperature_c' as independent variables X
    X = combined.loc[:, ['rainIntensity_mmh','temperature_c']]

    print('Assign hour')
    # Add hour to the matrix of independent variables
    X['hour'] = combined['HourMin'].apply(lambda x: int(x.split(':')[0]))

    print('Assign month')
    # Add month to the matrix of independent variables
    X['month'] = combined['Month']

    print('Assign weekday DISABLED')
    # Add weekday to the matrix of independent variables. 0 is Monday, 6 is Sunday.
    # THE SCRIPT GETS STUCK HERE SO DISABLED. Which is curious, because the same code works in the "Citybike-multiple..." file
    #X['weekday'] = combined['time'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").weekday())
    
    print('Variables assigned.')
    return X, y

def createAndTrainLinearModel(X, y):
    print('\n** Creating linear model **')
    print('X shape: ', X.shape)
    # Split the dataset into training and test sets 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state = 0)

    # LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    # Check how well the linear regression model fits to the observations
    R_2_train = regressor.score(X_train, y_train)
    print('R_2 score for training data:', R_2_train)
    R_2_test = regressor.score(X_test, y_test)
    print('R_2 score for testing data:', R_2_test)
    print ('Created linear model from historical data.')
    return regressor
