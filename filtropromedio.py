
import numpy as np
import matplotlib.pyplot as plt
from funcionesdef import*

#Datos a seleccionar
filename = "TERU042A00.23O"
sat = 'G04'
l1 = L1(filename, sat,30)
claves = list(p2.keys())
valores = list(p2.values())


def algoritmo_MAD(data= valores, window_size= 10,tiempo= 30):
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
    window_size = 10  # number of measurements in the sliding window
    threshold = 3  # threshold for cycle slip detection (standard deviations)
    plt.plot([i*tiempo for i in claves],valores,'.')
    #plt.plot(claves,valores,'.')
    times = []
    
    moving_average = np.convolve(valores, np.ones(window_size)/window_size, mode='valid')
    std = np.zeros(len(valores) - window_size + 1)
    for i in range(len(std)):
        std[i] = np.std(valores[i:i+window_size])
        
    for i in range(len(std)):
        if abs(valores[i+window_size-1] - moving_average[i]) > 2 * std[i]:
            times.append(claves[i+window_size-1])
            print(f"Salto de ciclo detectado en el instante de tiempo igual a {(claves[i+window_size-1])*30}.")
    plt.xlabel("Tiempo en segundos")
    plt.ylabel("P2 en metros")
    plt.title("Detector de ciclo usando sliding window")
    
    #Brechas de datos
    ti = []
    aux = np.diff(claves)
    for i in range(len(aux)):
        if aux[i]>30:  
            ti.append(i-1)
            ti.append(i) 
    for i in ti:
        plt.axvline(x  = claves[i+1]*30, color = 'g')
        
    for i in times:

        plt.plot(i*30,valores[i],'ro')# Para i-5 queda bonito
    plt.show()

def median_absolute_deviation(data, window_size):
    mad = []
    for i in range(window_size, len(data)):
        window = data[i-window_size:i]
        mad.append(np.median(np.abs(window - np.median(window))))
    return np.median(mad)


def get_key(val):
    for key, value in l1.items():
        if val == value:
            return key
    return None        
