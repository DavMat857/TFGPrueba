import numpy as np
from funcionesdef import*

#Análogo geo

#Datos a utilizar
filename = "datos/MAD1047A00.23O"
sat = 'G10'
datos = all_information2(filename)
l1 = L1(filename, sat)
l2 = L2(filename, sat)
io = combinacion_libre_ios(l1,l2)

#Visualización de L1 para cada satélite para L2, poner 4 en vez de 3
def visualizacion():
    graficar_frec(filename,3)


#Algoritmo
numero_muestras = 10


def algoritmo(datos = io, numero_muestras = numero_muestras,multiplo = 3, tiempo=1):

    
    graf_datos(datos, "Algoritmo_ionosfera",tiempo)
    media,std = selector_umbral(datos,numero_muestras)
    #umbral = media + std
    umbral =multiplo*std
    resultados = alg_sacar_saltos(datos,numero_muestras,umbral*multiplo)
    resultados = list(map(lambda x: x*tiempo, resultados))
    resultados = [i for i in resultados if i!=0]
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
          saltos.append(claves[0])
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
