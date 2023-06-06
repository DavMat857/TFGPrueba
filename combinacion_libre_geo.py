import numpy as np
from funcionesdef import*

#Datos a utilizar
filename = "datos/MAD1047A00.23O"
sat = 'G10'
datos = all_information2(filename)
l1 = L1(filename, sat)
l2 = L2(filename, sat)


#Visualización de L1 para cada satélite
def visualizacion():
    graficar_frec(filename,3)
    

#Algoritmo
numero_muestras = 10
umbral = 4.54

def algoritmo():
    
    geo = f1menosf2(l1,l2) #L1-L2
    graf_datos(geo, "combinación L1-L2")
    resultados = alg_sacar_saltos(geo,numero_muestras,umbral)
    return resultados

#Funciones auxiliares

"""Introduces datos, numero de muestras por paso y el umbral"""
def alg_sacar_saltos(datos,numero_muestras,umbral): 
    saltos = []
    
    for i in range(0,len(datos),numero_muestras):
    
        clave_items = list(datos.items())[i:i + numero_muestras]
        claves = [i[0] for i in clave_items]
        valores = [i[1] for i in clave_items]
        degree = 2
        
        coeffs = np.polyfit(claves,valores,degree)
        p  = np.poly1d(coeffs)
        pol = [p(n) for n in claves]
        
        if claves[len(claves)-1]- claves[0] > 30:
          saltos.append(claves[j])
        else:
            valor_real = np.array(valores)
            valor_pol = np.array(pol)
            error = np.abs(valor_real - valor_pol)

            for j in range(0,len(error)-1,1):
                if error[j]  > umbral:
                    saltos.append(claves[j])
                else:
                     saltos.append(0)
                     
    return np.array(saltos)

