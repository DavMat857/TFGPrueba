import tkinter as tk
from tkinter import messagebox

def obtener_elemento_seleccionado():
    # Obtener el elemento seleccionado de la lista
    seleccion = lista.curselection()
    if seleccion:
        elemento = lista.get(seleccion)
        messagebox.showinfo("Elemento seleccionado", "Has seleccionado: {}".format(elemento))
    else:
        messagebox.showwarning("Advertencia", "Debes seleccionar un elemento")

# Crear la ventana principal
ventana = tk.Tk()

# Crear una lista de opciones
opciones = ["Opción 1", "Opción 2", "Opción 3", "Opción 4"]

# Crear un widget de lista
lista = tk.Listbox(ventana)
lista.pack()

# Agregar las opciones a la lista
for opcion in opciones:
    lista.insert(tk.END, opcion)

# Crear un botón para obtener el elemento seleccionado
boton_seleccionar = tk.Button(ventana, text="Seleccionar", command=obtener_elemento_seleccionado)
boton_seleccionar.pack()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
