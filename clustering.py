import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from funcionesdef import*

#Datos seleccionados
filename = "MAD1060R001s.23O"
sat = 'G07'
frecuen = L1(filename,sat)    

# Con esto graficaremos la frecuencia L1 de todos los satélites 
def preprocesamiento():
    graficar_frec(filename, 4)
        
def algoritmo(datos,datos_por_paso,tiempo): 
    for i in range(0,len(datos),datos_por_paso):
        print("RANGO entre" , i*tiempo , (i+datos_por_paso)*tiempo)
        DBS(datos,i,i+datos_por_paso,tiempo)

def DBS(frec ,rango_min,rango_max,tiempo):
    valores = select_eps(frec,rango_min,rango_max,tiempo) #valores[0] me da el eps y valores[1] me da std
    if valores:
        grafica_DBSCAN(frec ,2 ,valores[0]+2*valores[1],rango_min,rango_max,tiempo) #Sumarle dos veces la desviación típica

def select_eps(frec,rango_min,rango_max,tiempo,n=3):
    
    infor = list(frec.items())[rango_min:rango_max]
    infor = [[i[0]*tiempo,i[1]] for i in infor]
    infor = np.array(infor)
    brecha_datos = np.diff(infor,axis=0)
    if max(brecha_datos[:,0])<3*tiempo: 
    
        phase_diff = np.diff(infor, axis = 0) 
        phase_diff = np.linalg.norm(phase_diff,axis = 1)
        std = np.std(phase_diff)
        
        phase_diff_abs = [abs(i) for i in phase_diff]
        mean = np.mean(phase_diff_abs)
        
        eps1 = seleccion_eps_EUCLIDEAN(infor,n,min(phase_diff_abs), max(phase_diff_abs))
        
        return eps1, std
    else:
        print("SALTO DE CICLO")
        
    
    
def seleccion_eps_EUCLIDEAN(datos ,n, minimo,maximo): # Voy a comentar las gráficas del silhouette
    

    eps = np.linspace(minimo,maximo, num=1000)
    
    sil = []
    for i in eps:
        db = DBSCAN(eps=i, min_samples=n, metric='euclidean').fit(datos)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        if len(set(labels))> 1:
            sil.append(metrics.silhouette_score(datos, labels))
        else:
            sil.append(0)
    maximo = max(sil)
    indice = sil.index(maximo)
    return eps[indice]

def grafica_DBSCAN(frec ,n ,eps,rango_min,rango_max,tiempo):
    
    
    infor = list(frec.items())[rango_min:rango_max]
    infor = [[i[0]*tiempo,i[1]] for i in infor]
    infor = np.array(infor) # array([[tiempo,distancia]])
    
    epsoptimo = eps #seleccion_eps_EUCLIDEAN(datos,n)
    
    db = DBSCAN(eps=epsoptimo, min_samples=n, metric='euclidean').fit(infor)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
        
    
    #SOLO GRAFICAR
    unique_labels = set(labels)
    print(unique_labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    
    plt.figure(figsize=(8,4))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]
    
        class_member_mask = (labels == k)
    
        xy = infor[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=5)
    
        xy = infor[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=3)
    
    plt.title('Estimated number of DBSCAN clusters: %d' % (len(unique_labels - {-1})))
    plt.show()