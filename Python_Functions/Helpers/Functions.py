# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:19:23 2024

@author: USUARIO
"""
from tensorflow.keras.models import load_model
import joblib
from .Comprobaciones import comprobacion_completo

#%%Define the selected regressor
def define_regressor(var, model):
    COMBO_model = {'Plas_Vs':'ANN','Max_Vs':'GBM','Fin_Vs':'GBM',
                   'Plas_D':'ANN','Max_D':'ANN','Fin_D':'ANN'}
    if model == "ANN":
        path_model = f"Helpers/Modelos_Entrenados/{model}_{var}.h5"
        regressor = load_model(path_model,compile=False)
    elif model in ["RF","GBM","LASSO"]:
        path_model = f"Helpers/Modelos_Entrenados/{model}_{var}.pkl"
        regressor = joblib.load(path_model) 
    elif model == "COMBO":
        if COMBO_model[var] == "ANN":
            path_model = f"Helpers/Modelos_Entrenados/{COMBO_model[var]}_{var}.h5"
            regressor = load_model(path_model,compile=False)
        elif COMBO_model[var] in ["RF","GBM","LASSO"]:
            path_model = f"Helpers/Modelos_Entrenados/{COMBO_model[var]}_{var}.pkl"
            regressor = joblib.load(path_model)
    else:
        raise ValueError(f"The option of ML model ({model}) is not available")
    return regressor

#%%Define the selected Scaler
def define_scaler(var):
    var_predict=["Plas_D","Max_D","Fin_D","Plas_Vs","Max_Vs","Fin_Vs"]
    if var=="X":
        path="Helpers/Scalers/ScalerX.pkl"
    elif var in var_predict:
        path=f"Helpers/Scalers/ScalerY_{var}.pkl"
    else:
        raise ValueError(f"The option of var_predict ({var}) is not available")
    scaler=joblib.load(path)
    return scaler

#%%Comprobation of format, range and normative requirements
def Comprobation(variables, i):
    cumplimiento = comprobacion_completo(variables)
    if cumplimiento == "SI":
        pass
    else:
        raise ValueError(f"Error on data (row {i}): {cumplimiento}")
    