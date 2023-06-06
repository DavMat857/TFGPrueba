from funcionesdef import*
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
#import imageio
import time

#Seleccionamos Datos

filename = "datos/GRA1065Q00.23O"
sat = 'G02'
datos = L1(filename , sat)
paso = 9

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
    


    
#Umbral 2*std + media
def algoritmo(datos = datos , paso = paso):
    claves = np.array(list(datos.keys()))
    valores = np.array(list(datos.values()))
    saltos = []
    
    for i in range(0, len(valores), paso):
       
        if i + paso < len(claves):
            brecha = max(np.diff(claves[i:i + paso]))
           
            if brecha > 5:
                print(f"Hay una brecha de datos entre {claves[i]} y {claves[i+paso]}")
            
            else:
                b,salt = dosaux(valores[i:i + paso],claves[i: i +paso])
                
                if b:
                    saltos.append(salt)
    return saltos

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
    media = np.mean(np.diff(residuals))
    std = np.std(np.diff(residuals))
    condicion = [i > 2*std + media for i in np.diff(residuals)]
    if True in condicion:
        b = True
        print(f"Salto de ciclo entre {claves[0]} y {claves[len(claves)-1]}")

        saltos = [claves[0],claves[len(claves)-1]]
    return b, saltos

