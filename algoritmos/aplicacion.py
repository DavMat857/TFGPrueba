import os
from funcionesdef import*
import tkinter as tk
from tkinter import messagebox, scrolledtext
from combinacion_libre_geo import algoritmo as alg_geo
from combinacion_libre_io import algoritmo as alg_io

carpeta_datos = 'datos'
archivos = [os.path.join(carpeta_datos, archivo) for archivo in os.listdir(carpeta_datos) if archivo.endswith("O") and os.path.isfile(os.path.join(carpeta_datos, archivo))]
list_fun = ['alg_geo','alg_io'] # Crear lista funciones
archivos_alg = ["--- Archivos ---"]+archivos+["--- Funciones ---"]+list_fun

def mostrar_informacion(elemento):
        # Crear una nueva ventana
    ventana_info = tk.Toplevel(ventana)
    
    # Configurar el tamaño y posición de la ventana
    ventana_info.geometry("400x300+200+200")
    
    # Configurar el título de la ventana
    ventana_info.title("Información")
    
    # Crear un widget de ScrolledText
    texto_info = scrolledtext.ScrolledText(ventana_info, width=50, height=10)
    texto_info.pack()
    
    # Agregar el texto al widget ScrolledText
    texto_info.insert(tk.INSERT, elemento)
    
    # Desactivar la edición del widget ScrolledText
    texto_info.configure(state='disabled')

def obtener_elemento_seleccionado():
    seleccion = lista.curselection()
    
    if seleccion:
        elementos_seleccionados = [lista.get(index) for index in seleccion]
        datos = elementos_seleccionados[0]
        algoritmo = elementos_seleccionados[1]
        l1 = L1(datos,'G10')
        #mostrar_informacion(l1.keys())
        ##############Hay que cambiar algo para que me deje 
        """sats = desplegable(ventana,satelites(datos))
        seleccion_sat = sats.curselection()
        seleccion = seleccion_sat
        if seleccion_sat:
            satelites_seleccionados = [sats.get(index) for index in seleccion_sat]
            print(satelites_seleccionados[0])"""
        ##############3333
        print(algoritmo)
        resultado = eval(algoritmo)(l1,10,3)
        resultado = [i for i in resultado if i!=0]
        mostrar_informacion(resultado)
        

    else:
        messagebox.showwarning("Advertencia", "Debes seleccionar al menos un elemento")

# Crear la ventana principal
ventana = tk.Tk()


def desplegable(ventana_actual , select):
    # Crear una lista de opciones
    opciones = select

    # Crear un widget de lista
    lista = tk.Listbox(ventana_actual, selectmode=tk.MULTIPLE)
    lista.pack()

    # Agregar las opciones a la lista
    for opcion in opciones:
        lista.insert(tk.END, opcion)

    # Crear un botón para obtener el elemento seleccionado
    boton_seleccionar = tk.Button(ventana_actual, text="Seleccionar", command=obtener_elemento_seleccionado)
    boton_seleccionar.pack()
    return lista


lista = desplegable(ventana,archivos_alg)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
