#!/usr/bin/env python3

"""
This module contains the functionality needed to train, validate, and forecast wheat yield
"""
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression, VarianceThreshold
  
# K-Fold Cross Validation
def kfold_cross_validation(data, model="ECMWF", region="Chaco húmedo sur", init=8, feature_names=["tmean_8"], no_of_features="all"):
    """Retrain, select features, and directly forecast yield on national level.
    
    params:
     - data: all features and yield on national level for all years
     - model: hindcast model to validate (default: ECMWF)
     - init: month of model initialization to validate (default:8)
     - augment: boolean, if train data should use SCM data in addition to ERA
     - no_of_features: the number of most correlated features with the target to be selected
     
    returns:
     - national_forecasts_by_year: dataframe with forecasted and observed national wheat yield for the selected model and month of initialization on cross validation
    """
    # Filter by model and init_month but also include observations that are used for model training
    cv_dataset = data.loc[((data["model"] == model) & (data["init_month"] == init) & (data["region"] == region))
                        | ((data["model"] == "ERA") & (data["init_month"] == 12) & (data["region"] == region))]
    # Dataframe where predictions are saved
    forecasts_by_year = cv_dataset.loc[(cv_dataset["model"] == "ERA"), ["year", "yield anomaly [%]", "yield_loss"]].assign(predicted=np.nan)  
    # Dataframe where final results are saved
    year_to_features = {}
    
    for season in list(range(1993,2017)):
        X_train = cv_dataset.loc[((cv_dataset["model"] == "ERA") & (cv_dataset["year"] != season)), feature_names].reset_index(drop=True)
        y_train = cv_dataset.loc[((cv_dataset["model"] == "ERA") & (cv_dataset["year"] != season)), "yield anomaly [%]"].reset_index(drop=True)
        
        pipeline = Pipeline([('scaler', StandardScaler()), 
                             ('selector', SelectKBest(f_regression, k=no_of_features)),
                             ('estimator', Ridge(alpha=8))])
        
        reg = pipeline.fit(X_train, y_train)  
        
        coefficients = reg["estimator"].coef_
        bias = reg["estimator"].intercept_
        features = reg["selector"].get_feature_names_out(feature_names)
        year_to_features[season] = features
        X_val = cv_dataset.loc[(cv_dataset["model"] == model)
                               & (cv_dataset["year"] == season), feature_names].reset_index(drop=True)
        
        y_predicted = reg.predict(X_val)[0]
        #print(y_predicted)
        #print(cv_dataset.loc[(cv_dataset["model"] == model)
        #                       & (cv_dataset["year"] == season), "yield anomaly [%]"])
        forecasts_by_year.loc[forecasts_by_year["year"] == season, "predicted"] = y_predicted
    
    return (forecasts_by_year, year_to_features)