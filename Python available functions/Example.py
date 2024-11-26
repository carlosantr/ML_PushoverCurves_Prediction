# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:19:23 2024

@author: USUARIO
"""
import pandas as pd
from Prediction_Function import prediction_Pushover_individual, prediction_Pushover_multiple

#%%Example of individual prediction
df_results_individual = prediction_Pushover_individual(Ny = 5, 
                                                       Nx = 5, 
                                                       Ly = 4, 
                                                       Lx = 5, 
                                                       Fc = 25, 
                                                       W = 25, 
                                                       B = 0.3, 
                                                       H = 0.4, 
                                                       Cuantia_C = 0.013, 
                                                       Cuantia_V_Sup = 0.006, 
                                                       Cuantia_V_Inf = 0.004)

#%%Example of multiple predictions
dataset = pd.read_excel("Helpers/Example_Dataset.xlsx")
df_results_multiple = prediction_Pushover_multiple(dataset,
                                                   comprobation=True)
