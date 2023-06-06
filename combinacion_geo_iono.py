import numpy as np
from funcionesdef import*

#Datos a utilizar
filename = "datos/MAD1047A00.23O"
sat = 'G10'
datos = all_information2(filename)
l1 = L1(filename, sat)
l2 = L2(filename, sat)
io = combinacion_libre_io(l1,l2)

  
#Vamos a graficar L1 y L2, las combinaciones libre de geometría e ionosfera
def visualizacion():
  
    l1menosl2 = f1menosf2(l1 , l2)
    plt.plot([i for i in l1.keys()],[j for j in l1.values()],'.',label = "L1")
    plt.plot([i for i in l2.keys()],[j for j in l2.values()],'.',label = "L2")
    plt.xlabel("Número de observación")
    plt.ylabel("Medidas de cada frecuencia")
    
    plt.plot([i for i in l1menosl2.keys()],[j for j in l1menosl2.values()],'.', label = "L1 - L2")
    
    plt.plot(list(io.keys()), list(io.values()), '.', label = "(f1^2*L1 - f2^2*L2) / (f1^2 - f2^2))" ) 
   
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    plt.show()
    
    alg_graf(f1menosf2(l1,l2),10,color='green')
    plt.show()
    alg_graf(io,10,color = 'red')
    plt.show()    

#Algoritmo
def algoritmo() :
  #Creación de listas donde almacenar resultados
    saltos_comunes = []
    duda_geo = []
    duda_ion = []
    
   #Obtención de saltos de ciclo para las combinaciones mencionadas y % datos en común
    geo = alg_sacar_saltos(f1menosf2(l1,l2),9,4.54)
    ion = alg_sacar_saltos(io,9,15.77)
    comp = geo == ion
    print(f"Coinciden en el {(list(comp).count(True)/len(comp))*100}% de los datos")
    
    for i in range(len(geo)):
        if geo[i] != ion[i] :
            if geo[i]!= 0:
                duda_geo.append(geo[i])
           # print(f"Hay que revisar que sucede entre {geo[i]} y {ion[i]}") # Este print puede ser útil
            else:
                duda_ion.append(ion[i])
        elif geo[i] == ion[i] and geo[i] !=0:
            saltos_comunes.append(i)
            
    print(f"Podemos afirmar con mayor seguridad que hay salto de ciclo en las observaciones {saltos_comunes}")
    print(f"Hay dudas de que haya salto de ciclo en geo para los instantes {duda_geo} y en ion para {duda_ion}")            
    return duda_geo,duda_ion
 
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
  
def alg_graf(datos : dict,numero_muestras,color):
   
    errores_totales = np.array([])
    
    e = []
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
          print(f"Salto de ciclo entre {claves[0]} y {claves[len(claves)-1]} por brecha de datos")
          
        else:
            valor_real = np.array(valores)
            valor_pol = np.array(pol)
            error = np.abs(valor_real - valor_pol)
            e.append(list(error))
            errores_totales = np.concatenate((errores_totales,error))
            plt.plot(claves,error,'.',color = color)

    media = np.mean(errores_totales)
    std = np.std(errores_totales)
    
    count = np.count_nonzero(errores_totales < media + std )
    porcent = round(100*count/len(errores_totales),2)
    plt.axhline(y=media+std, color='black', label =f"media + std = {round(media+std,2)}({porcent}%)")
    
    
    count = np.count_nonzero(errores_totales < media + 2*std )
    porcent = round(100*count/len(errores_totales),2)
    plt.axhline(y=media+2*std, color='blue', label =f"media + 2*std = {round(media+2*std,2)}({porcent}%)")
    
    count = np.count_nonzero(errores_totales < media + 3*std )
    porcent = round(100*count/len(errores_totales),2)
    plt.axhline(y=media+3*std, color='grey', label =f"media + 3*std = {round(media+3*std,2)}({porcent}%)")
    plt.xlabel("Número de observación")
    plt.ylabel("Residuos del polinomio de interpolación")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    return errores_totales



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
                    

            
