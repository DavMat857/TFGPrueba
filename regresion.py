from funcionesdef import*
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import imageio
import time

#Seleccionamos Datos

filename = "GRA1065Q00.23O"
sat = 'G02'
datos = C1(filename , sat)


def intro() -> None:
    print("Primero vamos a graficar L1 para todos los satélites")
    time.sleep(1)
    graficar_frec(filename, 0)
    print( "Seleccionamos un satélite")
    time.sleep(1)
    graficar_sat(filename, 0 , 'G02')
    
    ### ANALIZAMOS UMBRRALES
    print("Procedemos con el análisis del umbral\n graficando los residuos de un modelo de regresión lineal")
    time.sleep(5)
    


    dos(datos , 1)
    
#Umbral 2*std + media
def algoritmo(data = datos , paso = 9):
    claves = np.array(list(datos.keys()))
    valores = np.array(list(datos.values()))
    saltos = []
    
    for i in range(0, len(valores), paso):
       # print("entre")
        if i + paso < len(claves):
            
            brecha = max(np.diff(claves[i:i + paso]))
           #print(brecha)
            if brecha > 5:
                print(f"Hay una brecha de datos entre {claves[i]} y {claves[i+paso]}")
            
            else:
                b,salt = dosaux(valores[i:i + paso],claves[i: i +paso])
                
                if b:
                    saltos.append(salt)
    return saltos

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
        #print(f"Media {np.mean(residuals)} \n Desviación típica {np.std(residuals)})")
        #Plotear los cambios en los residuos
#        plt.ylabel("Residuos en metros")
#        plt.xlabel("Número de observaciones")
#        plt.plot(claves,residuals,'bo')
#        plt.show()
        saltos = [claves[0],claves[len(claves)-1]]
    #ESTABLECER UMBRAL
    return b, saltos





#Conseguir datos para otros casos
def residuos_paso(data):
    
    valores= list(data.values())
   
        
    data1 = np.array(valores[30:41])
    data2 = np.array(valores[41:52])
    x1 = np.arange(data1.size).reshape((-1, 1))
    x2 = np.arange(data2.size).reshape((-1, 1))
    
    #Ajustar un modelo de regresióno para los datos
    model1 = LinearRegression().fit(x1, data1)
    model2 = LinearRegression().fit(x2, data2)
        
    #Calcular los residuos
    residuals1 = data1 - model1.predict(x1)
    residuals2 = data2 - model2.predict(x2)
    print(residuals1, residuals2)
       
    












images = []

# 9== paso  imageio.mimsave('animacion.gif', images, fps=10)
def gif(data:list , paso: int,indicador = -1) -> None:
    for i in range(0, len(data), paso):
        gif_aux(data[i:i+paso],indicador + i)
        
def gif_aux(data,indicador): # graficar los residuos sin tener en cuenta el nº de observación
    #definir un numpy array
    data = np.array(data)
    colors = ['r', 'b', 'g', 'm']
    color = colors[indicador%4]
    #Definir el valor x crear 0 ,1 , 2 , ... nº observaciones
    x = np.arange(data.size).reshape((-1, 1))
    
    #Ajustar un modelo de regresióno para los datos
    model = LinearRegression().fit(x, data)
    
    #Calcular los residuos
    residuals = data - model.predict(x) 
    
    #Si lo quisiera en valor absoluto 
    # residuals = np.abs( data - model.predict(x))
    if len(data) == 9:
        #Plotear los cambios en los residuos
        plt.ylabel("Residuos en metros")
        plt.xlabel("Número de observaciones")
        
        plt.plot([i for i in range(9*(indicador),9*indicador+9,1)], residuals,'.',color = 'blue')
        
        plt.savefig("imagen{}.png".format(indicador))
        image = imageio.imread("imagen{}.png".format(indicador))
        images.append(image)
        #plt.show() #Esto si le doy me saca fotograma a fotograma sino me lo daria entero
#################OPCION EXTRA
    
    #Aplicar la transformada discreta de Fourier modificada (MDF) a los residuos para detectar el ciclo:
#from scipy.fftpack import rfft, irfft
#
#def mdf(residuals):
#    n = len(residuals)
#    r = np.zeros(n+1)
#    r[1:n+1] = residuals
#    r[0] = r[n]
#    a = r[:n] + 1j*r[n::-1]
#    b = np.real(irfft(1j*np.imag(rfft(a))))
#    return b[:n]
#
#cycle_slip = np.argmax(np.abs(mdf(residuals)))
