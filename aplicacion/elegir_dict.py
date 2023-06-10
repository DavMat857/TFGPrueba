import tkinter as tk
from tkinter import messagebox

def f(diccionario):
    # Realiza las operaciones deseadas utilizando el diccionario
    resultado = diccionario['clave1'] + diccionario['clave2']
    return resultado

def obtener_resultado(diccionario_seleccionado):
    try:
        resultado = f(diccionario_seleccionado)
        messagebox.showinfo("Resultado", "El resultado es: {}".format(resultado))
    except KeyError:
        messagebox.showerror("Error", "El diccionario no contiene las claves necesarias")

def seleccionar_diccionario(diccionarios):
    # Crea una ventana de selección de diccionarios
    ventana_seleccion = tk.Toplevel()
    ventana_seleccion.title("Seleccionar Diccionario")

    # Crea una lista de opciones para los diccionarios
    lista_diccionarios = tk.Listbox(ventana_seleccion)
    lista_diccionarios.pack()

    # Agrega los diccionarios a la lista de opciones
    for diccionario in diccionarios:
        lista_diccionarios.insert(tk.END, diccionario['nombre'])  # 'nombre' es una clave que identifica cada diccionario

    def obtener_diccionario_seleccionado():
        # Obtiene el índice del diccionario seleccionado
        indice_seleccionado = lista_diccionarios.curselection()
        if indice_seleccionado:
            diccionario_seleccionado = diccionarios[indice_seleccionado[0]]
            obtener_resultado(diccionario_seleccionado)
        else:
            messagebox.showwarning("Advertencia", "Debes seleccionar un diccionario")

    # Crea un botón para obtener el diccionario seleccionado
    boton_seleccionar = tk.Button(ventana_seleccion, text="Seleccionar", command=obtener_diccionario_seleccionado)
    boton_seleccionar.pack()

# Crear la ventana principal
ventana = tk.Tk()

# Definir los diccionarios disponibles
diccionarios = [
    {'nombre': 'Diccionario 1', 'clave1': 10, 'clave2': 20},
    {'nombre': 'Diccionario 2', 'clave1': 30, 'clave2': 40},
    {'nombre': 'Diccionario 3', 'clave1': 50, 'clave2': 60}
]

# Crear un botón para seleccionar el diccionario
boton_seleccionar = tk.Button(ventana, text="Seleccionar Diccionario", command=lambda: seleccionar_diccionario(diccionarios))
boton_seleccionar.pack()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
