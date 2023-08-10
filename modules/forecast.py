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
def kfold_cross_validation(data, model="ECMWF", init=8, augment=False, no_of_features=3):
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
    if init == 12: model = "ERA"
    cv_dataset = (data.loc[((data["model"] == model) & (data["init_month"] == init))
                               | ((data["model"] == "ERA") & (data["init_month"] == 12))])
    # Dataframe where interim results are saved
    national_forecasts_by_year = (pd.DataFrame(data={"year":list(range(1993,2017)), "predicted":np.zeros(24)})
                                  .merge(cv_dataset.loc[(cv_dataset["model"] == "ERA"), 
                                                        ["year", "yield anomaly [%]"]], on="year", how="left"))
    # Features
    relevant_columns = [c for c in cv_dataset.columns if c not in ["model", "init_month", "year", "yield [kg/ha]", "yield_trend [kg/ha]", "yield anomaly [%]"]]
    
    year_to_features = {}
    if augment: models_for_training = ["ERA", model]
    else: models_for_training = ["ERA"]
    for season in list(range(1993,2017)):
        X_train = cv_dataset.loc[((cv_dataset["model"].isin(models_for_training)) & (cv_dataset["year"] != season)), relevant_columns].reset_index(drop=True)
        y_train = cv_dataset.loc[((cv_dataset["model"].isin(models_for_training)) & (cv_dataset["year"] != season)), "yield anomaly [%]"].reset_index(drop=True)
        
        #print(season)
        #print(X_train)    
        pipeline = Pipeline([('scaler', StandardScaler()), 
                             ('var', VarianceThreshold()), 
                             ('selector', SelectKBest(f_regression, k=no_of_features)),
                             ('estimator', Ridge())])
        
        reg = pipeline.fit(X_train, y_train)  
        
        coefficients = reg["estimator"].coef_
        bias = reg["estimator"].intercept_
        features = reg["selector"].get_feature_names_out(relevant_columns)
        year_to_features[season] = features
        X_val = cv_dataset.loc[(cv_dataset["model"] == model)
                               & (cv_dataset["year"] == season), relevant_columns].reset_index(drop=True)
        
        y_predicted = reg.predict(X_val)[0]
        
        national_forecasts_by_year.loc[national_forecasts_by_year["year"] == season, "predicted"] = y_predicted
    
    return (national_forecasts_by_year, year_to_features)