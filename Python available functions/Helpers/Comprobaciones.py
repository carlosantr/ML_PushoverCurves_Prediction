# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:19:07 2024

@author: USUARIO
"""

from .Comprobacion_SCWB import comprobacion_norma
from numpy import round

#%%Formato de entrada
def comprobacion_formato(variables):
    variables_transformadas = {}
    cumplimiento = "SI"
    for var in variables.keys():
        if variables[var] != "":#Verificar si contiene algo
            if var in ["Nx", "Ny"]:
                if (isinstance(variables[var], float) & variables[var].is_integer())|isinstance(variables[var], int):
                    variables_transformadas[var]=int(variables[var])
                else:
                    cumplimiento = f"{var} must be a positive integer number"
                    break
            else:
                try:
                    variables_transformadas[var]=float(variables[var])
                except:
                    cumplimiento = f"{var} must be a number"  
                    break
            if variables_transformadas[var]<=0:
                cumplimiento = f"{var} must be a number greater than 0"  
                break
        else:
            cumplimiento = f"There is no value entered for {var}" 
            break
    return variables_transformadas, cumplimiento

#%%RANGOS
def comprobacion_rangos(variables):
    rangos ={'Ny':[1.99,5.01],
             'Nx':[1.99,5.01],
             'Ly':[2.49,4.01],
             'Lx':[3.99,8.01],
             'Fc':[16.99,35.01],
             'W':[9.99,30.01],
             'B':[0.24,0.51],
             'H':[0.29,0.66],
             'Cuantia_C':[0.0112,0.0278],
             'Cuantia_V_Sup':[0.005,0.0126],
             'Cuantia_V_Inf':[0.0033,0.0092]}
    cumplimiento = "SI"
    for var in variables.keys():
        if (variables[var] < rangos[var][0])|(variables[var] > rangos[var][1]):
            cumplimiento = f"Out of range for variable {var} ({rangos[var]})"
            break
    return cumplimiento

#%%Comprobacion norma
def comprobacion_norma_general(variables):
    LimH1=round(float(0.05*round((variables["Lx"]/16)/0.05)),2)#Beam height limit 1
    LimH2=round(float(0.05*round((variables["Lx"]/12)/0.05)),2)#Beam height limit 2
    LimB1=round(float(0.05*round((variables["H"]/1.4)/0.05)),2)#Beam base limit 1
    LimB2=round(float(0.05*round((variables["H"]/1.2)/0.05)),2)#Beam base limit 2
    cumplimiento = "SI"
    #C.21.3.5.1
    if variables["B"]<0.25:
        cumplimiento = "Does not comply with the norm C.21.3.5.1\n(B >= 0.25m)"
    #C.9.5.2.1
    if (variables["H"]<LimH1)|(variables["H"]>LimH2):
        cumplimiento = "Does not comply with the norm C.9.5.2.1\n(Lx/12 >= H >= Lx/16)"
    #C.10.4.1
    if variables["Lx"]/variables["B"]>50:
        cumplimiento = "Does not comply with the norm C.10.4.1\n(Lx/B > 50)"
    #Altura/Base
    if (variables["B"]<LimB1)|(variables["B"]>LimB2):
        cumplimiento = "It does not comply with the relationship between the height and base of beams\n(H/1.4 >= B >= H/1.2)"
    #C.3.21.3.6.2.2
    OK = comprobacion_norma(variables)
    if OK == 0:
        cumplimiento = "Does not comply with the norm C.3.21.3.6.2.2 of the Strong Column Weak Beam criterion [SCWB]\n(Mnc >= 1.2Mnb)"
    return cumplimiento

#%%Comprobacion
def comprobacion_completo(variables):
    variables_transformadas, cumplimiento = comprobacion_formato(variables)
    if cumplimiento=="SI":#Comprobación de formato
        cumplimiento = comprobacion_rangos(variables_transformadas)
        if cumplimiento=="SI":#Comprobación rango
            variables_transformadas["Fc"]=variables_transformadas["Fc"]*1000
            cumplimiento = comprobacion_norma_general(variables_transformadas)
            if cumplimiento=="SI":#Comprobación de norma
                return (cumplimiento)
            else:
                return (cumplimiento)
        else:
            return (cumplimiento)
    else:
        return (cumplimiento)
