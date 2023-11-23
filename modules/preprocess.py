#!/usr/bin/env python3

"""
This module contains the functionality needed to preprocess climate data
"""
import pandas as pd


def apply_basis_expansion(data):
    """
    apply basis expansion to SCM feature-dataframe and return as new dataframe, where original features are replaced with new ones.
    params:
        data: dataframe, with the original features; monthly tmean and monthly rainfall
    returns:
        data_expanded: dataframe, with tmean_squared, rain_squared, and tmean_times_rain features
    """ 
    # standardize data before multiplication LOYO (because of different scale of tmean and rain)
    standardized_data = []
    for year in data["year"].unique().tolist():
        X_train = data.loc[data["year"] != year, [c for c in data.columns if ("rain" in c) or ("tmean" in c)]].reset_index(drop=True)
        X_val = data.loc[(data["year"] == year) & (data["model"] != "ERA"), [c for c in data.columns if ("rain" in c) or ("tmean" in c)]].reset_index(drop=True)
        y_val = data.loc[(data["year"] == year) & (data["model"] != "ERA"), [c for c in data.columns if ("rain" not in c) and ("tmean" not in c)]].reset_index(drop=True)
        X_val_standardized = (X_val - X_train.mean()) / X_train.std(ddof=0)
        standardized_df = pd.concat([y_val, X_val_standardized], axis=1)
        standardized_data.append(standardized_df)
    df_standardized = pd.concat(standardized_data, ignore_index=True)
    
    # store features and target in variables for better readability
    X_temp = df_standardized.loc[:, [c for c in df_standardized.columns if ("tmean" in c)]]
    X_rain = df_standardized.loc[:, [c for c in df_standardized.columns if ("rain" in c)]]
    y = df_standardized.loc[:, [c for c in df_standardized.columns if ("rain" not in c) and ("tmean" not in c)]].reset_index(drop=True)

    # basis expansion to linear model
    X_tmean_squared = X_temp.mul(X_temp)
    X_rain_squared = X_rain.mul(X_rain)
    X_rain_tmean = X_rain * X_temp.values
    X_tmean_squared.columns = ["tmean_squared_{}".format("_".join(c.split("_")[1:])) for c in X_tmean_squared.columns]
    X_rain_squared.columns = ["rain_squared_{}".format("_".join(c.split("_")[1:])) for c in X_rain_squared.columns]
    X_rain_tmean.columns = ["tmean_rain_{}".format("_".join(c.split("_")[1:])) for c in X_rain_tmean.columns]
    
    # merge to feature dataframe
    X = (X_tmean_squared.merge(X_rain_squared.merge(X_rain_tmean, left_index=True, right_index=True), left_index=True, right_index=True))
    data_expanded = pd.concat([y, X], axis=1)
    
    return data_expanded