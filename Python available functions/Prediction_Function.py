# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 15:56:24 2024

@author: USUARIO
"""

import pandas as pd
from Helpers.Functions import define_regressor, define_scaler, Comprobation

#%%Prediction Function - Individual
def prediction_Pushover_individual(Ny,Nx,Ly,Lx,Fc,W,B,H,Cuantia_C,Cuantia_V_Sup,Cuantia_V_Inf,
                                   var_predict=["Plas_D","Max_D","Fin_D","Plas_Vs","Max_Vs","Fin_Vs"],
                                   model_predict=["COMBO","ANN","RF","GBM","LASSO"],
                                   comprobation=True,
                                   normalized=True):
    """
    Ny: Number of stories [#] (range: [])
    Nx: Number of spans [#]
    Ly: Column height [m]
    Lx: Beam length [m]
    Fc: Compressive strength of concrete [MPa]
    W: Distributed total load on beams, including columns and beams weight [kN/m]
    B: Base for beams and columns (square) [m]
    H: Height for beams [m]
    Cuantia_C: Reinforcement ratio of column [--]
    Cuantia_V_Sup: Reinforcement ratio for top of the beams [--] 
    Cuantia_V_Inf: Reinforcement ratio for bottom of the beams [--]
    ___________________________________________________________________
    *The next variables are optional according to the user preference*    
    var_predict: The varibles to be predicted
        Plas_D: Building roof drift ratio for the Yielding point
        Max_D: Building roof drift ratio for the Maximum point
        Fin_D: Building roof drift ratio for the Failure point
        Plas_Vs: Building base shear for the Yielding point
        Max_Vs: Building base shear for the Maximum point
        Fin_Vs: Building base shear for the Failure point
    model_predict: The Machine Learning models to do the predictions
        COMBO: The combo, which combine the best models combination on each output variable (i.e., the best models for Plas, Max, and Failure points on Vs and δ)
        ANN: Artificial Neural Networks    
        RF: Random Forests
        GBM: Gradient Boosting Machines
        LASSO: Lasso regression
    comprobation: Set if the normative requirements, range requirements, and format requirements are checked [True or False]
    normlized: Set if the returned value is the normalized value for Vs (Vs/Wt) and δ (δ/ht) or not [True or False]
    """   
    v_graph={'Plas_D':'δ - Yield','Max_D':'δ - Max','Fin_D':'δ - Failure',
             'Plas_Vs':'Vs - Yield','Max_Vs':'Vs - Max','Fin_Vs':'Vs - Failure'}

    df_prediction = pd.DataFrame(index=model_predict, columns=v_graph.values())#Dataframe to save predictions
    X = pd.DataFrame({'Ny':[Ny],
                      'Nx':[Nx],
                      'Ly':[Ly],
                      'Lx':[Lx],
                      'Fc':[Fc],
                      'W':[W],
                      'B':[B],
                      'H':[H],
                      'Cuantia_C':[Cuantia_C],
                      'Cuantia_V_Sup':[Cuantia_V_Sup],
                      'Cuantia_V_Inf':[Cuantia_V_Inf]})
    if comprobation:
        for i in range(len(X)):
            Comprobation(X.loc[i], i)
    X["Fc"]=X["Fc"]*1000
    scalerX = define_scaler("X")
    X_scaled = scalerX.transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    for var in v_graph.keys():
        scalerY = define_scaler(var)
        for model in model_predict:
            #Import model
            regressor=define_regressor(var, model)
            #Prediction
            prediction_scaled = regressor.predict(X_scaled)
            prediction = scalerY.inverse_transform(prediction_scaled.reshape(-1, 1)).ravel()
            #Saving the prediction
            df_prediction.loc[model, v_graph[var]] = prediction
    #Comprobation of normalization
    if normalized:
        pass
    elif normalized == False:
        Wt = X["W"]*X["Nx"]*X["Lx"]*X["Ny"]
        ht = X["Ny"]*X["Ly"]
        for col in df_prediction.columns:
            if "Vs" in col:
                df_prediction[col]=df_prediction[col]*Wt[0]
            elif "δ" in col:
                df_prediction[col]=df_prediction[col]*ht[0]
    else:
        raise ValueError("normalized must be True or False")
    return df_prediction

#%%Prediction function - Dataframe
def prediction_Pushover_multiple(X,
                                 var_predict=["Plas_D","Max_D","Fin_D","Plas_Vs","Max_Vs","Fin_Vs"],
                                 model_predict=["COMBO","ANN","RF","GBM","LASSO"],
                                 comprobation=False,
                                 normalized=True):
    """
    X is a dataframe with the next columns (each row is a prediction):
        Ny: Number of stories [#] (range: [])
        Nx: Number of spans [#]
        Ly: Column height [m]
        Lx: Beam length [m]
        Fc: Compressive strength of concrete [MPa]
        W: Distributed total load on beams, including columns and beams weight [kN/m]
        B: Base for beams and columns (square) [m]
        H: Height for beams [m]
        Cuantia_C: Reinforcement ratio of column [--]
        Cuantia_V_Sup: Reinforcement ratio for top of the beams [--] 
        Cuantia_V_Inf: Reinforcement ratio for bottom of the beams [--]
        
        ***************************************
        The columns must be in the same order and must have the same name
        i.e., X.columns = ['Ny', 'Nx', 'Ly', 'Lx', 'Fc', 'W', 'B', 'H', 'Cuantia_C', 'Cuantia_V_Sup', 'Cuantia_V_Inf']
        ***************************************
    ___________________________________________________________________
    *The next variables are optional according to the user preference*
    var_predict: The varibles to be predicted
        Plas_D: Building roof drift ratio for the Yielding point
        Max_D: Building roof drift ratio for the Maximum point
        Fin_D: Building roof drift ratio for the Failure point
        Plas_Vs: Building base shear for the Yielding point
        Max_Vs: Building base shear for the Maximum point
        Fin_Vs: Building base shear for the Failure point  
    model_predict: The Machine Learning models to do the predictions
        COMBO: The combo, which combine the best models combination on each output variable (i.e., the best models for Plas, Max, and Failure points on Vs and δ)
        ANN: Artificial Neural Networks    
        RF: Random Forests
        GBM: Gradient Boosting Machines
        LASSO: Lasso regression
    comprobation: Set if the normative requirements, range requirements, and format requirements are checked [True or False]
    normlized: Set if the returned value is the normalized value for Vs (Vs/Wt) and δ (δ/ht) or not [True or False]
    
    """
    v_graph={'Plas_D':'δ - Yield','Max_D':'δ - Max','Fin_D':'δ - Failure',
             'Plas_Vs':'Vs - Yield','Max_Vs':'Vs - Max','Fin_Vs':'Vs - Failure'}
    #Verifying if X have the necessary columns
    X_col = ['Ny', 'Nx', 'Ly', 'Lx', 'Fc', 'W', 'B', 'H', 'Cuantia_C', 'Cuantia_V_Sup', 'Cuantia_V_Inf']
    if list(X.columns) != X_col:
        raise ValueError(f"The dataframe X does not have the correct columns: {X_col}")
    if comprobation:
        for i in range(len(X)):
            Comprobation(X.loc[i], i)
    X["Fc"]=X["Fc"]*1000
    #Creating prediction columns
    col = [f"{model}: {v_graph[var]}" for var in var_predict for model in model_predict]
    df_prediction = pd.DataFrame(columns=col)
    #Scaling X
    scalerX = define_scaler("X")
    X_scaled = scalerX.transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    for var in var_predict:
        scalerY = define_scaler(var)
        for model in model_predict:
            #Import model
            regressor=define_regressor(var, model)
            #Prediction
            prediction_scaled = regressor.predict(X_scaled)
            prediction = scalerY.inverse_transform(prediction_scaled.reshape(-1, 1)).ravel()
            #Saving the predictions
            df_prediction[f"{model}: {v_graph[var]}"] = prediction
    #Comprobation of normalization
    if normalized:
        pass
    elif normalized == False:
        Wt = X["W"]*X["Nx"]*X["Lx"]*X["Ny"]
        ht = X["Ny"]*X["Ly"]
        for col in df_prediction.columns:
            if "Vs" in col:
                df_prediction[col]=df_prediction[col]*Wt
            elif "δ" in col:
                df_prediction[col]=df_prediction[col]*ht
    else:
        raise ValueError("normalized must be True or False")
    return df_prediction


