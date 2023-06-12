
import numpy as np
import matplotlib.pyplot as plt
from funcionesdef import*

#Datos a seleccionar
filename = "datos/TERU042A00.23O"
sat = 'G04'
l1 = L1(filename, sat)
claves = list(l1.keys())
valores = list(l1.values())


def algoritmo_MAD(data= valores, window_size= 10,tiempo= 1):
    n = len(data)
    threshold = 3 * median_absolute_deviation(data, window_size)
    slip_flags = np.zeros(n, dtype=int)
    for i in range(window_size, n):
        window = data[i-window_size:i]
        if np.any(np.abs(window - np.median(window)) > threshold):
            print(f"Salto de ciclo detectado en el instante de tiempo igual a {(i)*tiempo}.")
            slip_flags[i] = i*tiempo
            
    return slip_flags
  
  
def algoritmo_DT(valores = valores,claves = claves,tiempo = 30):
    window_size = 10  
    threshold = 3  
    
    times = []
    
    moving_average = np.convolve(valores, np.ones(window_size)/window_size, mode='valid')
    std = np.zeros(len(valores) - window_size + 1)
    for i in range(len(std)):
        std[i] = np.std(valores[i:i+window_size])
        
    for i in range(len(std)):
        if abs(valores[i+window_size-1] - moving_average[i]) > 2 * std[i]:
            times.append(claves[i+window_size-1]*tiempo)
            
    return times

def median_absolute_deviation(data, window_size):
    mad = []
    for i in range(window_size, len(data)):
        window = data[i-window_size:i]
        mad.append(np.median(np.abs(window - np.median(window))))
    return np.median(mad)

