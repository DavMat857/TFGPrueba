import numpy as np
from funcionesdef import*
from combinacion_libre_io import combinacion_libre_io, selector_umbral, alg_sacar_saltos
#Datos a utilizar

filename = "datos/MAD1047A00.23O"
sat = 'G10'
datos = all_information2(filename)
l1 = L1(filename, sat)
l2 = L2(filename, sat)
geo = f1menosf2(l1,l2)
io = combinacion_libre_io(l1,l2)
numero_muestras = 10
   
#Algoritmo
def algoritmo() :# umbral y nº de observaciones
  #Creación de listas donde almacenar resultados
    saltos_comunes = []
    duda_geo = []
    duda_ion = []
    umbral_geo = selector_umbral(geo,numero_muestras)[0]+selector_umbral(geo,numero_muestras)[1]
    umbral_io = selector_umbral(io,numero_muestras)[0]+ selector_umbral(io,numero_muestras)[1]
   #Obtención de saltos de ciclo para las combinaciones mencionadas y % datos en común
    saltos_geo = alg_sacar_saltos(f1menosf2(l1,l2),numero_muestras,umbral_geo)
    saltos_ion = alg_sacar_saltos(io,numero_muestras,umbral_io)
    comp = saltos_geo == saltos_ion
    print(f"Coinciden en el {(list(comp).count(True)/len(comp))*100}% de los datos")
    
    for i in range(len(saltos_geo)):
        if saltos_geo[i] != saltos_ion[i] :
            if saltos_geo[i]!= 0:
                duda_geo.append(saltos_geo[i])
           # print(f"Hay que revisar que sucede entre {geo[i]} y {ion[i]}") # Este print puede ser útil
            else:
                duda_ion.append(saltos_ion[i])
        elif saltos_geo[i] == saltos_ion[i] and saltos_geo[i] !=0:
            saltos_comunes.append(i)
            
    print(f"Podemos afirmar con mayor seguridad que hay salto de ciclo en las observaciones {saltos_comunes}")
    print(f"Hay dudas de que haya salto de ciclo en geo para los instantes {duda_geo} y en ion para {duda_ion}")            
    return duda_geo,duda_ion
 


  