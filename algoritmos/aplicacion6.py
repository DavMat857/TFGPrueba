import os
from funcionesdef import*
import tkinter as tk
from tkinter import messagebox, scrolledtext
from combinacion_libre_geo import algoritmo as alg_geo
from combinacion_libre_io import algoritmo as alg_io
from clustering import algoritmo as alg_clus
import threading

carpeta_datos = 'datos'
archivos = [os.path.join(carpeta_datos, archivo) for archivo in os.listdir(carpeta_datos) if archivo.endswith("O") and os.path.isfile(os.path.join(carpeta_datos, archivo))]
list_fun = ['alg_geo','alg_io','alg_clus'] # Crear lista funciones
frecuencias = ['L1','L2']
satelites = ['G0'+str(i) for i in range(1,10)]+ ['G'+str(i) for i in range(10,36)]
archivos_alg = ["--- Archivos ---"]+archivos+["--- Funciones ---"]+list_fun+["--- Frecuencias ---"]+frecuencias

def leer_contenido_archivo(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read()  # Lee todo el contenido del archivo en una sola cadena
    return contenido

informacion = leer_contenido_archivo("datos/read.txt")


def mostrar_informacion(elemento,titulo):
    ventana_info = tk.Toplevel(ventana)
    ventana_info.geometry("400x300+200+200")
    ventana_info.title(titulo)
    
    texto_info = scrolledtext.ScrolledText(ventana_info, width=50, height=10)
    texto_info.pack()
    texto_info.insert(tk.INSERT, elemento)
    texto_info.configure(state='disabled')

def obtener_elemento_seleccionado():
    seleccion = lista.curselection()
    
    if seleccion:
        elementos_seleccionados = [lista.get(index) for index in seleccion]
        datos = elementos_seleccionados[0]
        algoritmo = elementos_seleccionados[1]
        frecuencia = elementos_seleccionados[2]
        l1 = eval(frecuencia)(datos,'G10')
        
        resultado = eval(algoritmo)(l1,10,3)
        resultado = [i for i in resultado if i!=0]
        mostrar_informacion(resultado,"resultados")
        
    else:
        messagebox.showwarning("Advertencia", "Debes seleccionar al menos un elemento")

# Crear la ventana principal
ventana = tk.Tk()

# Mostrar mensaje persistente al inicio del script
mensaje_persistente = mostrar_informacion(informacion,"Guía sobre ficheros")
#hilo_mensaje_persistente = threading.Thread(target=mostrar_mensaje_persistente, args=(mensaje_persistente,))
#hilo_mensaje_persistente.start()

def desplegable(ventana_actual , select):
    opciones = select
    lista = tk.Listbox(ventana_actual, selectmode=tk.MULTIPLE)
    lista.pack()

    for opcion in opciones:
        lista.insert(tk.END, opcion)

    boton_seleccionar = tk.Button(ventana_actual, text="Seleccionar", command=obtener_elemento_seleccionado)
    boton_seleccionar.pack()
    return lista

lista = desplegable(ventana,archivos_alg)

ventana.mainloop()
