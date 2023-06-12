
from funcionesdef import*
import numpy as np


#Datos a utilizar
filename = "datos/MAD1047A00.23O"
sat = 'G10'
datos = all_information2(filename)
l1 = L1(filename, sat)
l2 = L2(filename, sat)
geo = f1menosf2(l1,l2)#L1-L2
numero_muestras = 10

#Visualización de L1 para cada satélite para L2, poner 4 en vez de 3
def visualizacion():
    graficar_frec(filename,3)
    

#Algoritmo

def algoritmo(datos = geo,numero_muestras=numero_muestras, tiempo = 1):
     
    graf_datos(datos, "combinación libre geometría", tiempo)
    resultados = alg_sacar_saltos(datos,numero_muestras)
    resultados = list(map(lambda x: x*tiempo, resultados))
    return resultados


#Funciones auxiliares

"""Introduces datos, numero de muestras por paso y el umbral"""
def alg_sacar_saltos(datos,numero_muestras): 
    saltos = []
    i = 1
    
    claves = [int(i) for i in list(datos.keys())]
    valores = list(datos.values())
    #Primer polinomio
    pol, umbral= crear_pol(claves[0:numero_muestras],valores[0:numero_muestras])
    while i<len(datos)-10 :
    #for i in range(0,len(datos),numero_muestras):
        
        if claves[i]- claves[i] > 30:
          saltos.append(claves[i])
          i=i+1
          pol, umbral= crear_pol(claves[i:i+numero_muestras],valores[i:i+numero_muestras])
        
        else:
            valor_real = valores[i]
            valor_pol = pol(claves[i])
            error = np.abs(valor_real - valor_pol)

            
            if error  > umbral:
                saltos.append(claves[i])
                i=i+1
                pol, umbral= crear_pol(claves[i:i+numero_muestras],valores[i:i+numero_muestras])
        
            else:
                saltos.append(0)
                i=i+1
                     
    return np.array(saltos)

#Creación de un polinomio
def crear_pol(claves,valores):
    
    degree = 2
        
    coeffs = np.polyfit(claves,valores,degree)
    p  = np.poly1d(coeffs)
    pol = [p(n) for n in claves]
    
    valor_real = np.array(valores)
    valor_pol = np.array(pol)
    error = np.abs(valor_real - valor_pol)
    umbral = np.mean(error) + np.std(error)
    
    return p,umbral
