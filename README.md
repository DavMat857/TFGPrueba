# TFG: MÉTODOS HEURÍSTICOS PARA DETECCIÓN DE DISCONTINUIDADES EN LA RECEPCIÓN DE SATÉLITES DE POSICIONAMIENTO
#### Autor: David Labrador Merino
Observación: la creación de este repositorio no está basado en otros y la autoría me pertenece al 100% 

Vamos a presentar distintos scripts para la detección de saltos de ciclo:

## Para el preprocesado de los ficheros Rinex 2.11 usaremos:

* `funcionesdef.py`: contiene la información relativa a las funciones utilizadas. 
*  `preprocesado.ipynb`: muestra ejemplos de utilización del anterior script.

## Algoritmos para la detección del ciclos[Todos están explicados en el TFG]:
__Observación__: los algoritmos siguen la misma estructura
1. Datos a seleccionar.
2. Visualización de los datos.
3. Algoritmo.
4. Función auxiliar.

* `combinacion_libre_geo.py`: es un algoritmo que utiliza la combinación libre de geometría
* `combinacion_geo_iono.py`: es un algoritmo que utiliza la combinación libre de geometría e ionosfera, realizando comparaciones entre ellas.
	* Crear solo geo y solo io
*  `clustering.py`: es un algoritmo basado en DBSCAN para la detección de saltos de ciclo.
*  `filtropromedio.py`: es un algoritmo que utiliza el filtro promedio móvil, y el umbral está relacionado con la desviación típica y con ABS.
	 * Quitar gráficas.   
	 * Crear listas para almacenar resultados.
* `regresion.py`: algoritmo basado en la regresión lineal para la detección de saltos de ciclo.
	* Implementar los nuevos r^2, s, r para la creación de mejores modelos.
* `contraste.py`: es un contraste de hipótesis usando t-Student para `regresion.py`. 
	* Eliminar bibliotecas innecearias

