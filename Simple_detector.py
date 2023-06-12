#1.- sliding()
#2.-detect_cycle_slip()
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('G:/Mi unidad/4 curso/Universidad/TFG/observaciones/')

from funcionesdef import*
filename = "TERU042A00.23O"




# read Rinex file
#l1 = P2(filename,'G04',30)
p2 = P2(filename,'G04')
claves = list(p2.keys())
valores = list(p2.values())


def get_key(val):
    for key, value in l1.items():
        if val == value:
            return key
    return None
#################PRIMERO
def sliding(valores = valores,claves = claves,tiempo = 30):
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
    #Brechas de tiempo
    ti = []
    aux = np.diff(claves)
    for i in range(len(aux)):
        if aux[i]>30:  
            ti.append(i-1)
            ti.append(i) 
    for i in ti:
        plt.axvline(x  = claves[i+1]*30, color = 'g')
        
    for i in times:
#        plt.axvline(x=i*30, color='r')    
        plt.plot(i*30,valores[i],'ro')# Para i-5 queda bonito
    plt.show()
###################SEGUNDO
def detect_cycle_slip(data= valores, window_size= 10,tiempo= 30):
    n = len(data)
    threshold = 3 * median_absolute_deviation(data, window_size)
    slip_flags = np.zeros(n, dtype=int)
    for i in range(window_size, n):
        window = data[i-window_size:i]
        if np.any(np.abs(window - np.median(window)) > threshold):
            print(f"Salto de ciclo detectado en el instante de tiempo igual a {(i)*tiempo}.")
            slip_flags[i] = i*tiempo
            
    
    return slip_flags

def median_absolute_deviation(data, window_size):
    mad = []
    for i in range(window_size, len(data)):
        window = data[i-window_size:i]
        mad.append(np.median(np.abs(window - np.median(window))))
    return np.median(mad)

def graficarL1(filename, tiempos):
    satelites = ['10', 'G01', 'G03', 'G04', 'G08', 'G09', 'G14', 'G17', 'G19', 'G21', 'G31']
    for i in satelites:
        frec = P2(filename, i , 30)
#        ejey = []
#        ejex = []
#        for j in range(len(frec)):
#            pass
        plt.plot([int(i) for i in frec.keys()],[int(j) for j in frec.values()],'.',label = str(i))
        plt.legend()
        plt.show()
        
