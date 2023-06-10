import os
from funcionesdef import*

carpeta_datos = 'datos'
archivos = [os.path.join(carpeta_datos, archivo) for archivo in os.listdir(carpeta_datos) if archivo.endswith("O") and os.path.isfile(os.path.join(carpeta_datos, archivo))]
import tkinter as tk
from tkinter import messagebox, scrolledtext

from combinacion_libre_geo import algoritmo as alg_geo
from combinacion_libre_io import algoritmo as alg_io

list_fun = [alg_geo,alg_io]
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
    # Obtener el elemento seleccionado de la lista
    seleccion = lista.curselection()
    
    if seleccion:
        pass
    elemento = lista.get(seleccion)
        
    l1 = L1(elemento,'G10')
        #mostrar_informacion(l1)

    seleccion2 = lista2.curselection()
    if seleccion2:
        elemento2 = lista2.get(seleccion2)
        result = elemento2(l1,10,3)
        mostrar_informacion(result)
            #mostrar_informacion(elemento2)
            #messagebox.showinfo("Elemento seleccionado", "Has seleccionado: {}".format(elemento))
        
    else:
        messagebox.showwarning("Advertencia", "Debes seleccionar un elemento")

# Crear la ventana principal
ventana = tk.Tk()


def desplegable(ventana_actual = ventana, select = archivos):
    # Crear una lista de opciones
    opciones = select

    # Crear un widget de lista
    lista = tk.Listbox(ventana_actual)
    lista.pack()

    # Agregar las opciones a la lista
    for opcion in opciones:
        lista.insert(tk.END, opcion)

    # Crear un botón para obtener el elemento seleccionado
    boton_seleccionar = tk.Button(ventana_actual, text="Seleccionar", command=obtener_elemento_seleccionado)
    boton_seleccionar.pack()
    return lista

lista = desplegable()
lista2 = desplegable(ventana, list_fun)
# Iniciar el bucle principal de la aplicación
ventana.mainloop()
