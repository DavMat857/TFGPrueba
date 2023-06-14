import numpy as np
from funcionesdef import*
from combinacion_libre_io import  selector_umbral, alg_sacar_saltos
#Datos a utilizar

filename = "datos/MAD1047A00.23O"
sat = 'G10'
datos = all_information2(filename)
l1 = L1(filename, sat)
l2 = L2(filename, sat)
geo = f1menosf2(l1,l2)
io = combinacion_libre_ios(l1,l2)
numero_muestras = 10
   
#Algoritmo
def algoritmo(io=io,geo=geo,numero_muestras=numero_muestras, tiempo = 1) :# umbral y nº de observaciones
  #Creación de listas donde almacenar resultados
    graf_datos(geo,"combinacion libre de geometria", tiempo)
    saltos_comunes = []
    duda_geo = []
    duda_ion = []
#    umbral_geo = selector_umbral(geo,numero_muestras)[0]+selector_umbral(geo,numero_muestras)[1]
#    umbral_io = selector_umbral(io,numero_muestras)[0]+ selector_umbral(io,numero_muestras)[1]
    
    umbral_geo = 3*selector_umbral(geo,numero_muestras)[1]
    umbral_io = 3*selector_umbral(io,numero_muestras)[1]
#   #Obtención de saltos de ciclo para las combinaciones mencionadas y % datos en común
    saltos_geo = alg_sacar_saltos(f1menosf2(l1,l2),numero_muestras,umbral_geo)
    saltos_ion = alg_sacar_saltos(io,numero_muestras,umbral_io)
    #Comunes
    comp = [saltos_geo[i] for i in range(min(len(saltos_geo),len(saltos_ion))) if abs(saltos_geo[i]-saltos_geo[i])<10]
    print(f"Coinciden en el {(list(comp).count(True)/len(comp))*100}% de los datos")
    comp = [i for i in comp if i !=0]
    duda_geo= set(saltos_geo) - set(comp)
    duda_ion= set(saltos_ion) - set(comp)

            
    print(f"Podemos afirmar con mayor seguridad que hay salto de ciclo en las observaciones {comp}")
    print(f"Hay dudas de que haya salto de ciclo en geo para los instantes {duda_geo} y en ion para {duda_ion}")     

    duda_geo = list(map(lambda x: x*tiempo,duda_geo))
    duda_ion = list(map(lambda x: x*tiempo, duda_ion))       
    return duda_geo,duda_ion
 


  
