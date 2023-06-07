from regresion2 import*
from scipy.stats import t
import scipy.stats as stats

#Seleccionamos datos a utilizar
filename = "datos/GRA1065Q00.23O"
sat ='G02'
l1 = L1(filename,sat)
datos = l1
paso = 10

#Algoritmo de comprobación
def comprobacion( datos=datos, paso=paso):
    lista_saltos = algoritmo(datos,paso)
    saltos_comprobacion = [] #Lista de bool
    for i in lista_saltos:
        try:
            
            data_before = residuos([datos[i] for i in range(i-paso,i,1)])
            data_after = residuos([datos[i] for i in range(i,i+paso,1)])
            saltos_comprobacion.append(t_student(data_before,data_after))
            
        except:
            KeyError
            saltos_comprobacion.append(False)
    return saltos_comprobacion

#Funciones auxiliares
def residuos(data):
    data = np.array(data)
    
    #Definir el valor x crear 0 ,1 , 2 , ... nº observaciones
    x = np.arange(data.size).reshape((-1, 1))
    
    #Ajustar un modelo de regresióno para los datos
    model = LinearRegression().fit(x, data)
    
    #Calcular los residuos
    residuals = data - model.predict(x) 
    
    #Si lo quisiera en valor absoluto 
    residuals = np.abs( data - model.predict(x))
    return residuals
  
def t_student(data_before, data_after):

    mean_before = np.mean(data_before)
    std_before = np.std(data_before)
    
    mean_after = np.mean(data_after)
    std_after = np.std(data_after)
    
    n_before = len(data_before)
    n_after = len(data_after)
    
    s = np.sqrt(((n_before-1)*(std_before**2) + (n_after-1)*(std_after**2))/(n_before+n_after-2))
    t = (mean_after - mean_before) / (s * np.sqrt(1/n_before + 1/n_after))
    
    p = 1 - stats.t.cdf(t, n_before+n_after-2)
   #print(p)
    if p<0.05:
    #    print("Hay un salto de ciclo")
        return True
    else:
    #    print("No hay nada")
        return False
    
