# Vamos a añadir los tipos de los parámetros a introducir en esta primera parte del código con el fin de facilitar su entendimiento
# con el menor número de comentarios

import matplotlib.pyplot as plt

######################################Funciones auxiliares
def words(s: str) -> list:  
    lista = []
    aux = ""
    indicador = 0
    for i in range(len(s)):
        if s[i] =="\n":
            lista.append(aux)
        
        elif (s[i] != " "):
            aux += s[i]
            indicador = 0
        else:
            if (aux != "" or indicador>17): #Es un caso especial
                lista.append(aux)
                indicador = 0
            aux = ""
            indicador += 1
            
    return lista 

def date(a : str) -> dict: #Coloca la fecha e instante de observación junto con los satélites activos en ese momento
    D = {}
    aux = ""
    for i in range(len(a)):
        try:
            if(a[i] != int(a[i]) ):
                aux += a[i]

        except ValueError:
            D[aux] = []
            break

    aux = ""

    i =2
    while (i<len(a)):
        try:
            if(a[i] != int(a[i]) ):
                aux += a[i]
                i+=1
        except ValueError:
            if(len(aux))<1:
                aux+= a[i]
            if(len(aux)>1):
                D[aux] = []
                aux = ""
            else:
                i+=1
                aux += a[i]
                i+=1
    
    D[aux] = []
    return D



def all_information2(filename : str) -> dict: #Lee el archivo Rinex y lo procesa en un diccionario
    f  = open(filename, 'r')
    lines = f.readlines()
    inicio = lines.index('                                                            END OF HEADER\n')
    lines = lines[inicio+1:] # El inicio contiene información que no es necesaria
    lista = []
    indice_lista = 0

    for i in range(len(lines)):
        
        if (len((lines[i]))<20 and len(words(lines[i-1])) == 8):
            lista.append(words(lines[i]))
            
        elif (len(words(lines[i]))) == 2 and('G' in words(lines[i])[len(words(lines[i]))-1] ):
            lista[len(lista)-1][7]+=(words(lines[i])[1])
        
        elif (len(lines[i]) <20 and len(lines[i-1])>40) or lines[i]=='\n' :
            pass
           
        else:
            lista.append(words(lines[i]))
            
            indice_lista +=1
    
    k = 1
    SD = {}
    r = 0
    for i in (lista):  
         if(len(i)==8 ):

            D = date(i[len(i)-1])
            for j in (list(D.keys())):
                
                D[j] = lista[r]
                
                r+=1
            
            SD[str(k)] = D
            k+=1
    return (SD)

###### Vamos a mostrar las funciones más útiles para trabajar con un archivo de tipo Rinex 2.11

def unafrecuencia(filename : str , numero : int,sat : str) -> dict: # Me devuelve la información acerca de una frecuencia
    datos = all_information2(filename)
    frec  = {} 
    for i in range(1,3601,1) :
        if str(i) in datos.keys() and sat in datos[str(i)] and len(datos[str(i)][sat])>4:
           
            frec[int(str(i))] = float(datos[str(i)][sat][numero])
            
    return frec

#Funciones específicas que me devuelven información de una medida de fase o código

def C1(filename : str ,sat : str ) -> dict:
    return unafrecuencia(filename,0,sat)


def P2(filename : str ,sat : str ) -> dict:
    return unafrecuencia(filename,1,sat)

def L1(filename : str ,sat : str ) -> dict:
    return unafrecuencia(filename,3,sat)


def L2(filename : str ,sat : str ) -> dict:
    return unafrecuencia(filename,4,sat) 


def f1menosf2(f1 : dict ,f2: dict) -> dict:
    
    F ={}
    
    N = max(list(f1.keys())[len(f1)-1] , list(f2.keys())[len(f2)-1])    
    
    for i in range(N+1):
        if i in f1.keys() and i in f2.keys():
            F[i] = f1[i] - f2[i]
    return F

#Detecta una brecha de datos
def brecha(tiempos : list) -> list:
    saltos_ciclo = []
    
    indicador = tiempos[0]
    for i in tiempos[1:]:
        if i - indicador > 60:
            print("SALTO DE CICLO ENTRE", indicador, i)
            saltos_ciclo.append((indicador,i))
        indicador = i
        
    return saltos_ciclo



def satelites(filename : str ) -> list:

    datos = all_information2(filename)
    cjto = set()
    lista = []
    for i in (datos.keys()):

        cjto.update(set(datos[i].keys()))

    for j in cjto:
        if j[0] == 'G':
            lista.append(j)
    return lista


def graficar_frec(filename : str, frec : int) -> None:#Se puede optimizar bastante aunque no es determinante en este caso
    sats = satelites(filename)
    
    for i in sats:
        datos = unafrecuencia(filename,frec, i)
        frecue = ['C1', 'P2', 'P5', 'L1' , 'L2' , 'L5' ]
        plt.title(i)
        plt.ylabel(f"{frecue[frec]} en metros")
        plt.xlabel("Tiempo en segundos")
        plt.plot([i for i in datos.keys()] , [j for j in datos.values()], '.b')
        
        plt.show()

def graficar_sat(filename : str , frec : int , sat : str) -> None:
    if frec == 0 :
        datos = C1(filename, sat)

    elif frec == 1 :
        datos = P2(filename, sat)

    elif frec == 3 : 
        datos = L1(filename, sat)

    elif frec == 4:
        datos = L2(filename, sat)
    
    frecue = ['C1', 'P2', 'P5', 'L1' , 'L2' , 'L5' ]

    plt.title(sat)
    plt.ylabel(f"{frecue[frec]} en metros")
    plt.xlabel("Tiempo en segundos")
    plt.plot([i for i in datos.keys()] , [j for j in datos.values()], '.b')
    plt.show()


def graf_datos(datos: dict, titulo: str) -> None:
    plt.title(titulo)
    plt.plot([i for i in datos.keys()] , [j for j in datos.values()], '.b')
    plt.show()
