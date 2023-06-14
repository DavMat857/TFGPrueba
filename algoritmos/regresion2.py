from funcionesdef import*
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
#import imageio
import time
import pandas as pd
#Seleccionamos Datos

filename = "datos/GRA1065Q00.23O"
sat = 'G27'
l1 = L1(filename , sat)
l2 = L2(filename, sat)
datos = f1menosf2(l1,l2)
paso = 10

#Visualización
def visualizacion() :
    print("Primero vamos a graficar L1 para todos los satélites")
    time.sleep(1)
    graficar_frec(filename, 4)
    print( "Seleccionamos un satélite")
    time.sleep(1)
    graficar_sat(filename, 4, 'G02')
    
    ### ANALIZAMOS UMBRRALES
    print("Procedemos con el análisis del umbral\n graficando los residuos de un modelo de regresión lineal")
    time.sleep(5)
 #########################################################   
def resultados(filename = filename):
    D={}
    sats = satelites(filename)
    for i in sats:
        l1 = L1(filename , i)
        l2 = L2(filename, i)
        datos = f1menosf2(l1,l2)
        saltos = algoritmo(datos,9,1)
        D[i]= saltos
    return D


def generar_tabla():
    #saltos_ciclo = resultados(filename)
     max_length = max(len(saltos) for saltos in saltos_ciclo.values())

# Rellenar las listas con NaN hasta tener la misma longitud
     saltos_ciclo = {satelite: saltos + [float('nan')] * (max_length - len(saltos)) for satelite, saltos in saltos_ciclo.items()}

# Crear DataFrame con las listas de distintas longitudes
     df_saltos = pd.DataFrame(saltos_ciclo)
     
     df_saltos.to_csv('tabla_saltos.csv', index=False)
 
###################################################
        
#Umbral 2*std 
def algoritmo(datos = datos , paso = paso,tiempo =1):
    graf_datos(datos,"Algoritmo_regresion",tiempo)
    claves = np.array(list(datos.keys()))
    valores = np.array(list(datos.values()))
    resultados = []
    
    for i in range(claves[0], len(valores), paso):
       
        if i + paso < len(claves):
            brecha = max(np.diff(claves[i:i + paso]))
           
            if brecha > 30:
                #print(f"Hay una brecha de datos entre {claves[i]} y {claves[i+paso]}")
                resultados.append(claves[i])
                #i = i + paso
                pass
            else:
                b,salt = dosaux(valores[i:i + paso],claves[i: i +paso])
                
                if b:
                    resultados += salt
    resultados = list(map(lambda x: x*tiempo, resultados))
    return resultados

#funciones auxiliares
def dosaux(data,claves): # graficar los residuos sin tener en cuenta el nº de observación
    #definir un numpy array
    saltos = []
    b = False
    data = np.array(data)
    
    #Definir el valor x crear 0 ,1 , 2 , ... nº observaciones
    x = np.arange(data.size).reshape((-1, 1))
    
    #Ajustar un modelo de regresióno para los datos
    model = LinearRegression().fit(x, data)

    #Calcular los residuos
    residuals = data - model.predict(x) 
    
    #Si lo quisiera en valor absoluto 
    residuals = np.abs( data - model.predict(x))
    media = np.mean((residuals))
    std = np.std(residuals)
    condicion = [i >media + 2*std  for i in (residuals)]
    
    if True in condicion:
        b = True
        #print(f"Salto de ciclo entre {claves[0]} y {claves[len(claves)-1]}")

        for i in range(len(condicion)):
            if condicion[i]==True:
                saltos.append(claves[i])
    return b, saltos


from sklearn.metrics import r2_score

def r2(valores,estimados):
    r2 = r2_score(valores,estimados)
    return r2    
