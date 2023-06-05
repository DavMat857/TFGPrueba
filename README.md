# TFG: MÉTODOS HEURÍSTICOS PARA DETECCIÓN DE DISCONTINUIDADES EN LA RECEPCIÓN DE SATÉLITES DE POSICIONAMIENTO
#### Autor: David Labrador Merino
Observación: la creación de este repositorio no está basado en otros y la autoría me pertenece al 100% 

Vamos a presentar distintos scripts para la detección de saltos de ciclo:

Para el preprocesado de los ficheros Rinex 2.11 usaremos:

* `funcionesdef.py`: contiene la información relativa a las funciones utilizadas. 
*  `preprocesado.ipynb`: muestra ejemplos de utilización del anterior script.

Algoritmos para la detección del ciclos:

* `combinacion_geo_iono.py`: es un algoritmo que utiliza la combinación libre de geometría e ionosfera, realizando comparaciones entre ellas.
*  `cluster.py`: es un algoritmo basado en DBSCAN para la detección de saltos de ciclo.
