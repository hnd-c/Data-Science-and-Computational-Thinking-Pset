# -*- coding: utf-8 -*-
# Problem Set 5: Modeling Temperature Change
# Name:Hem N Chaudhary
# Collaborators:None
# Time: couple of days

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2000)
TESTING_INTERVAL = range(2000, 2017)

##########################
#    Begin helper code   #
##########################

def standard_error_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by a linear
            regression model
        model: a numpy array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]


class Dataset(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Dataset instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_daily_temps(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_temp_on_date(self, city, month, day, year):
        """
        Get the temperature for the given city at the specified date.

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified date and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year {} is not available".format(year)
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

##########################
#    End helper code     #
##########################

    def get_yearly_averages(self, cities, years):
        """
        For each year in the given range of years, computes the average of the
        annual temperatures in the given cities.

        Args:
            cities: a list of the names of cities to include in the average
                annual temperature calculation
            years: a list of years to evaluate the average annual temperatures at

        Returns:
            a 1-d numpy array of floats with length = len(years). Each element in
            this array corresponds to the average annual temperature over the given
            cities for a given year.
        """

        # NOTE: TO BE IMPLEMENTED IN PART 4B OF THE PSET
        ans=[]
        for year in years:
            average=0
            for city in cities:
                temperaturearray=self.get_daily_temps(city, year)
                average+=np.mean(temperaturearray)
            ans.append(average/len(cities))
        
        return np.array(ans)
            
        
def linear_regression(x, y):
    """
    Calculates a linear regression model for the set of data points.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points

    Returns:
        (m, b): A tuple containing the slope and y-intercept of the regression line,
                both of which are floats.
    """
    x_bar=np.mean(x)
    y_bar=np.mean(y)
    
    m_num=[]
    m_den=[]
    for i in range(len(x)):
        m_num.append((x[i]-x_bar)*(y[i]-y_bar)) #slope=y2-y2/x2-x1
        m_den.append((x[i]-x_bar)*(x[i]-x_bar))
    m=np.sum(m_num)/np.sum(m_den)
    b=y_bar-m*x_bar   #y=mx+c
    
    return (float(m),float(b))

def squared_error(x, y, m, b):
    '''
    Calculates the squared error of the linear regression model given the set
    of data points.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        m: The slope of the regression line
        b: The y-intercept of the regression line


    Returns:
        a float for the total squared error of the regression evaluated on the
        data set
    '''
    sqerror=[]
    for i in range(len(y)):
        y_line=m*x[i]+b
        sqerror.append((y[i]-y_line)*(y[i]-y_line)) #error=sum of (y-ypred)^2
    
    return np.sum(sqerror)




def generate_models(x, y, degrees):
    """
    Generates a list of polynomial regression models with degrees specified by
    degrees for the given set of data points

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        degrees: a list of integers that correspond to the degree of each polynomial
            model that will be fit to the data

    Returns:
        a list of numpy arrays, where each array is a 1-d numpy array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    num_array=[]
    for i in range(len(degrees)):
        num_array.append(np.polyfit(x,y,degrees[i]))
    
    return num_array
        


def evaluate_models(x, y, models, display_graphs=False):
    """
    For each regression model, compute the R-squared value for this model and
    if display_graphs is True, plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (i.e. the model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        Degree of your regression model,
        R-squared of your model evaluated on the given data points,
        and standard error/slope (if this model is linear).

    R-squared and standard error/slope should be rounded to 4 decimal places.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the R-squared value for each model
    """
    rsqr=[]
    for model in models:
        y_pred=[]
        for i in range(len(x)):
            y_pred.append(np.polyval(model,x[i])) #prediced y
        r2value=r2_score(y,y_pred)      #r^2 of y and y_predicted
        rsqr.append(r2value)
        
        if len(model)==2:#look for linear model
            sderror=str(round(np.std(y)/(np.sqrt(len(y))*model[0]),4))
        else:
            sderror='model is not linear'
        
        if display_graphs:  
            plt.scatter(x,y,color='b',label='Data')
            plt.plot(x,y_pred,'r',label='Fit of degree ' + str(len(model)-1) + ',Rsquare= ' +str(round(r2value,4))+\
                ' standard error/slope =' + sderror)
            plt.legend(loc='best')
            plt.xlabel("Years")
            plt.ylabel("Temperature(0C)")
            plt.show()
        
        
        
    return rsqr
            


def find_extreme_trend(x, y, length, positive_slope):
    """
    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        length: the length of the interval
        positive_slope: a boolean whose value specifies whether to look for
            an interval with the most extreme positive slope (True) or the most
            extreme negative slope (False)

    Returns:
        a tuple of the form (i, j, m) such that the application of linear (deg=1)
        regression to the data in x[i:j], y[i:j] produces the most extreme
        slope m, with the sign specified by positive_slope and j-i = length.

        In the case of a tie, it returns the first interval. For example,
        if the intervals (2,5) and (8,11) both have slope 3.1, (2,5,3.1) should be returned.

        If no intervals matching the length and sign specified by positive_slope
        exist in the dataset then return None
    """
    slopeint=0
    x1=0
    x2=0
    for i in range(len(x)-length+1):
        slope=generate_models(x[i:i+length], y[i:i+length],[1])[0][0] #finding the slope
        if positive_slope:
            if slope>slopeint and abs(slope-slopeint)>1e-8: #positive extreme
                slopeint=slope
                x2=i+length
                x1=i
        else:
            if slope<slopeint and abs(slope-slopeint)>1e-8:  #negative extreme
                slopeint=slope
                x2=i+length
                x1=i
    
    if slopeint==0:  #slope didn't change
        return None
    else:
        return (x1,x2,slopeint)

def find_all_extreme_trends(x, y):
    """
    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        
    Returns:
        a list of tuples of the form (i,j,m) such that the application of linear
        regression to the data in x[i:j], y[i:j] produces the most extreme
        positive OR negative slope m, and j-i=length. 

        The returned list should have len(x) - 1 tuples, with each tuple representing the
        most extreme slope and associated interval for all interval lengths 2 through len(x).
        If there is no positive or negative slope in a given interval length L (m=0 for all
        intervals of length L), the tuple should be of the form (0,L,None).

        The returned list should be ordered by increasing interval length. For example, the first 
        tuple should be for interval length 2, the second should be for interval length 3, and so on.

        If len(x) < 2, return an empty list
    """
    if len(x)<2:
        return []
    else:
        ans=[]
        for i in range(2,len(x)+1):
            slope_pos=find_extreme_trend(x, y,i,True)
            slope_neg=find_extreme_trend(x, y,i,False)
            
            if slope_pos==None and slope_neg==None: #both are none
                ans.append((0,i,None))
            elif slope_pos==None:            #positve slope is valid
                ans.append(slope_neg)
            elif slope_neg==None:           #negative slope is valid
                ans.append(slope_pos)  
            
            else:       #slopes are differnt 
                if abs(abs(slope_pos[2])-abs(slope_neg[2]))>1e-8:  #positive is extreme
                    ans.append(slope_pos)
                else:                                          #negative slope is extreme
                    ans.append(slope_neg)
    return ans 


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    ans=0
    for i in range(len(y)):
        ans+=(y[i]-estimated[i])**2 #definition; (y-y_est)^2
    
    return np.sqrt(ans/len(y)) #sqrt(ans/no of samples)
        



def evaluate_models_testing(x, y, models, display_graphs=False):
    """
    For each regression model, compute the RMSE for this model and if
    display_graphs is True, plot the test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    RMSE should be rounded to 4 decimal places.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N test data sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N test data sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the RMSE value for each model
    """
    RMSE=[]
    for model in models:
        y_pred=[]
        for i in range(len(x)):
            y_pred.append(np.polyval(model,x[i]))
        r2value=round(rmse(y,y_pred),4) #same as evaluete models; different definition
        RMSE.append(r2value)
        
        
        if display_graphs:
            plt.scatter(x,y,color='b',label='Data')
            plt.plot(x,y_pred,'r',label='Fit of degree ' + str(len(model)-1) + ',RMSE= ' +str(round(r2value,4)))
            plt.legend(loc='best')
            plt.xlabel("Years")
            plt.ylabel("Temperature(0C)")
            plt.show()
        
        
        
    return RMSE
    



if __name__ == '__main__':
    ##################################################################################
    # Problem 4A: DAILY TEMPERATURE
    # dataseet=Dataset('data.csv')
    # x=[]
    # y=[]
    # for i in range(1961,2017):
    #     x.append(i)
    #     y.append(dataseet.get_temp_on_date('SAN FRANCISCO', 12, 25, i))
    
    # genmodel_result=evaluate_models(x, y,generate_models(x, y, [1]),True)
        

    ##################################################################################
    # Problem 4B: ANNUAL TEMPERATURE
    # dataseet=Dataset('data.csv')
    # x=[]
    # for i in range(1961,2017):
    #     x.append(i)
        
    # y=dataseet.get_yearly_averages(['SAN FRANCISCO'], x)
    
    # genmodel_result=evaluate_models(x, y,generate_models(x, y, [1]),True)
    

    ##################################################################################
    # Problem 5B: INCREASING TRENDS
    # dataseet=Dataset('data.csv')
    
    # x=[]
    # for i in range(1961,2017):
    #     x.append(i)
        
    # y=dataseet.get_yearly_averages(['TAMPA'], x)
    # c=find_extreme_trend(x, y, 30, True)
    
    # genmodel_result=evaluate_models(x[c[0]:c[1]], y[c[0]:c[1]],generate_models(x[c[0]:c[1]], y[c[0]:c[1]], [1]),True)
    

    ##################################################################################
    # Problem 5C: DECREASING TRENDS
    # dataseet=Dataset('data.csv')
    
    # x=[]
    # for i in range(1961,2017):
    #     x.append(i)
        
    # y=dataseet.get_yearly_averages(['TAMPA'], x)
    # c=find_extreme_trend(x, y, 15, False)
    
    # genmodel_result=evaluate_models(x[c[0]:c[1]], y[c[0]:c[1]],generate_models(x[c[0]:c[1]], y[c[0]:c[1]], [1]),True)
    
    

    ##################################################################################
    # Problem 5D: ALL EXTREME TRENDS


    ##################################################################################
    # Problem 6B: PREDICTING
    #Training set
    # dataseet=Dataset('data.csv')
    # x=[]
    # for i in range(1961,2000):
    #     x.append(i)
        
    # y=dataseet.get_yearly_averages(CITIES, x)
    # models=generate_models(x, y, [2,10])
    # genmodel_result=evaluate_models(x, y,models,True)
    
    # #Test set
    # dataseet=Dataset('data.csv')
    # x=[]
    # for i in range(2000,2017):
    #     x.append(i)
        
    # y=dataseet.get_yearly_averages(CITIES, x)
    
    # model_result=evaluate_models_testing(x, y, models, True)
    ##################################################################################
    pass