#1.- sliding()
#2.-detect_cycle_slip()
import numpy as np
import matplotlib.pyplot as plt
from funcionesdef import*

filename = "datos/TERU042A00.23O"




datos = L2(filename,'G10')

#################PRIMERO FILTRO PROMEDIO MÓVIL

def algoritmo(datos = datos,tamaño_ventana = 10, tiempo = 1):
    
    #times = []
    #saltos = []
    graf_datos(datos,"",tiempo)
    claves = list(datos.keys())
    valores = list(datos.values())

    resultados_std = umbral_std(claves,valores,tamaño_ventana,tiempo)
    resultados_mad = umbral_mad(claves,valores,tamaño_ventana,tiempo)
    print("La primera lista usa el umbral std, el otro el umbral mad")
    return resultados_std , resultados_mad
    
    #################

def umbral_std(claves, valores, tamaño_ventana, tiempo):

    moving_average = np.convolve(valores, np.ones(tamaño_ventana)/tamaño_ventana, mode='valid')
    resultados = []

    std = np.zeros(len(valores) - tamaño_ventana + 1)
    for i in range(len(std)):
        std[i] = np.std(valores[i:i+tamaño_ventana]) #Cada i es la desv.tip de i hasta i+10
        
    for i in range(len(std)):
        if claves[i+1]-claves[i]>30:
            #brecha de datos
            resultados.append(claves[i+tamaño_ventana-1]*tiempo)

        else:    
            if abs(valores[i+tamaño_ventana-1] - moving_average[i]) >   2*std[i]:
                #times.append(claves[i+tamaño_ventana-1])
                #print(f"Salto de ciclo detectado en el instante de tiempo igual a {(claves[i+window_size-1])*tiempo}.")
                resultados.append(claves[i+tamaño_ventana-1]*tiempo)

    return resultados

def umbral_mad(claves, valores, tamaño_ventana, tiempo):

    moving_average = np.convolve(valores, np.ones(tamaño_ventana)/tamaño_ventana, mode='valid')
    resultados = []

    mad = np.zeros(len(valores) - tamaño_ventana + 1)
    for i in range(len(mad)):
        window = valores[i:i+tamaño_ventana]
        mad[i] = np.median(np.abs(window - np.median(window)))
        
    for i in range(len(mad)):
        if claves[i+1]-claves[i]>30:
            #brecha de datos
            resultados.append(claves[i+tamaño_ventana-1]*tiempo)

        else:    
            if abs(valores[i+tamaño_ventana-1] - moving_average[i]) >  2*mad[i]:
                
                resultados.append(claves[i+tamaño_ventana-1]*tiempo)

    return resultados


########################Aquí los crearía para ventanas
###################SEGUNDO Es como el anterior con otro umbral revisar
def detect_cycle_slip(datos= datos, tamaño_ventana= 10,tiempo= 30):#Arreglar
    valores = list(datos.values())
    claves = list(datos.keys())

    n = len(datos)
    threshold = 2 * median_absolute_deviation(valores, tamaño_ventana)
    slip_flags = np.zeros(n, dtype=int)
    for i in range(tamaño_ventana, n):
        window = valores[i-tamaño_ventana:i]

        if claves[i]-claves[i-1]>30:
            slip_flags[i] = i*tiempo

        else:

            if np.any(np.abs(window - np.median(window)) > threshold):
                #print(f"Salto de ciclo detectado en el instante de tiempo igual a {(i)*tiempo}.")
                slip_flags[i] = i*tiempo
            
    
    return slip_flags

def median_absolute_deviation(data, window_size):
    mad = []
    for i in range(window_size, len(data)):
        window = data[i-window_size:i]
        mad.append(np.median(np.abs(window - np.median(window))))
    return np.median(mad)
