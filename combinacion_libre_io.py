import numpy as np
from funcionesdef import*

def combinacion_libre_io(l1, l2):
    
    D = {}
    
    l1_data = np.array(list(l1.values()))
    l2_data = np.array(list(l2.values()))
    
    F1 = 1575.42e6
    F2 = 1227.60e6
    
    datos = (l1_data* (F1**2) - l2_data * (F2**2 )) / (F1**2 - F2**2)
    datos= list(datos)
    
    D = dict(zip(list(l1.keys()),datos))
    return D

#Datos a utilizar
filename = "datos/MAD1047A00.23O"
sat = 'G10'
datos = all_information2(filename)
l1 = L1(filename, sat)
l2 = L2(filename, sat)
io = combinacion_libre_io(l1,l2)

#Visualización de L1 para cada satélite para L2, poner 4 en vez de 3
def visualizacion():
    graficar_frec(filename,3)


#Algoritmo
numero_muestras = 10


def algoritmo(datos = io, numero_muestras = numero_muestras):

    
    graf_datos(datos, "Combinación libre io")
    media,std = selector_umbral(datos,numero_muestras)
    umbral = media + std
    resultados = alg_sacar_saltos(datos,numero_muestras,umbral)
    return resultados

#Obtención de umbral
def selector_umbral(datos : dict,numero_muestras):
   
    errores_totales = np.array([])
    
    e = []
    for i in range(0,len(datos),numero_muestras):
        
        
        clave_items = list(datos.items())[i:i + numero_muestras]
        claves = [i[0] for i in clave_items]
        valores = [i[1] for i in clave_items]
        degree = 2
        
        coeffs = np.polyfit(claves,valores,degree)
        p  = np.poly1d(coeffs)
        pol = [p(n) for n in claves]
        
       
        if claves[len(claves)-1]- claves[0] > 30:
          print(f"Salto de ciclo entre {claves[0]} y {claves[len(claves)-1]} por brecha de datos")
          
        else:
            valor_real = np.array(valores)
            valor_pol = np.array(pol)
            error = np.abs(valor_real - valor_pol)
            e.append(list(error))
            errores_totales = np.concatenate((errores_totales,error))
            

    media = np.mean(errores_totales)
    std = np.std(errores_totales)
    
    return media,std

#Funciones auxiliares
def combinacion_libre_io(l1, l2):
    
    D = {}
    
    l1_data = np.array(list(l1.values()))
    l2_data = np.array(list(l2.values()))
    
    F1 = 1575.42e6
    F2 = 1227.60e6
    
    datos = (l1_data* (F1**2) - l2_data * (F2**2 )) / (F1**2 - F2**2)
    datos= list(datos)
    
    D = dict(zip(list(l1.keys()),datos))
    return D

def alg_sacar_saltos(datos,numero_muestras,umbral): 
#Si los errores mayor que un valor entonces salto de ciclo y marcar valores
    saltos = []
    
    for i in range(0,len(datos),numero_muestras):
        #print("Analizamos",number,numero_muestras)
        
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
            #print(error)
            for j in range(0,len(error)-1,1):
                if error[j]  > umbral:
                    saltos.append(claves[j])
                else:
                     saltos.append(0)
                     
    return np.array(saltos)