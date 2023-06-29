#!/usr/bin/env python3

"""
This module contains the functionality needed to detrend time series of crop yields.
"""
import numpy as np
import matplotlib.pyplot as plt
from collections.abc import Iterable
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.linear_model import LinearRegression, TheilSenRegressor, HuberRegressor, RANSACRegressor

    
def regression_detrending(time_series, x_col="year", y_col="value", decomposition="additive", polynomial=1, regressor=LinearRegression()):
    """
    apply regression detrending.
    params:
        time_series: dataframe to be detrended
        x_col: string, the column indicating the year
        y_col: string, the column indicating the quantity to be detrended
        decomposition: string, one of additive or multiplicative
        polynomial: int, the order of regression
        regressor: regressor object from sklearn.linear_model
    returns:
        data: dataframe containing new column with detrended series
    """
    data = time_series.copy()
    
    x = np.array(data[x_col]).reshape(-1, 1)
    y = np.array(data[y_col]).reshape(-1, 1)
    
    # create array of the specified order of polynomials
    result = np.zeros((x.shape[0], polynomial+1))
    
    result[:, 0] = x[:, 0] 
    for i in range(2, polynomial+1):
        result[:, i-1] = np.power(x, i)[:, 0]
    x = result
    
    # Perform LOOCV and obtain predictions
    loo = LeaveOneOut()
    y_new = cross_val_predict(regressor, x, y, cv=loo)
   
    y_new = list(flatten(y_new))
    y = list(flatten(y))
    
    data["trend_estimated [t/ha]"] = y_new 
   
    if decomposition not in ["additive", "multiplicative"]: 
        print("decomposition must be additive or multiplicative")
        return None
    if decomposition == "additive":
        data["value_detrended [t/ha]"] = [a_i - b_i for a_i, b_i in zip(y, y_new)]
    if decomposition == "multiplicative":
        data["value_detrended [%]"] = [(a_i - b_i)/b_i for a_i, b_i in zip(y, y_new)]
    
    return data


def plot_time_series(time_series, to_plot=["value"], labels=["raw yield"], ax=None):
    """
    plot a time series of yield data including a trend estimation.
    params:
        time_series: dataframe, raw data for the plot and the trend estimation
        to_plot: string, column name that indicates which column should be plotted
        trend_estimator: string, indicating the estimation technique
        ax: pyplot ax to plot the data on
    returns:
        plot: pyplot plot
    """
    data = time_series.copy()
    data = data.dropna(subset=to_plot)
    
    column_to_label = dict(zip(to_plot, labels))
    
    if ax is None:
        ax = plt.gca()
    for col in to_plot:
        plot = ax.plot(data["year"], data[col], label=column_to_label[col]);
            
    ax.set_ylabel("yield");
    ax.legend();
    ax.set_xlabel("year");
    
    return plot


def flatten(xs):
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x