

# Proyecto 3 de Base de Datos




## Integrantes

| Nombre y Apellidos | Código de alumno |
|-|-|
|Victor Ostolaza | 201910049 |
|Jorge Vásquez	| 201310292 |
|Jorge Rebosio | 201820025|

## RTree

Con las ayuda de la libreria Rtree creamos los indices Rtree para cada muestra de fotos. La funcion para crear los indexfiles se llama `buildFinalIndex` se encuentra dentro del archivo build.py y va a generar los archivos Rtree_{size}.idx. Estos archivos servirán para cargar el Rtree a memoria al momento de realizar las búsquedas. 

## Sequential
Creamos sequential files para cada muestra de fotos. Esto lo realizamos con la funcion `buildFiles` que está dentro de el archivo python.py. Se van a generar los archivos Sequential_{size}.json, se guardaran, la direccion y el vector caracteristico de cada foto. 


## Pruebas Funcionales KNN Search

Se implemento dos tipos de funciones para la busqueda KNN, el primero es el KNN-sequential y el segundo es el Knn-Rtree. Ambas funciones se encuentran dentro del archivo search.py. 

Por un lado, para  la busqueda Knn-Rtree se va a cargar a disco el archivo Rtree_{size}.idx  con la ayuda de la libreria Rtree . Se va a llamar al metodo `nearest` para encontrar los k mas cercanos, y luego en el archivo Sequential_{size}.json se va a obtener la direccion de los fotos resultantes.

Por otro lado , la busqueda Knn Sequential, va a carga el archivo Sequential_{size}.json en bloques de 100 objetos. Esto para no agotar la memoria principal . Los objetos se van a introducir dentro un `min-heap`de tamano k para obtener los k mas cercanos. 


Para las pruebas funconales del KNN Search, la variable k tomó el valor de 8 . Se hizo el testing para cada tamano de imagenes, luego se grafico los tiempos del KNN tree y KNN Sequential



| Test  | Size  |KNN - Rtree | KNN- Secuencial| 
| :------------ |:---------------:| -----:| ------:|
| 1 | 100 |  0.2263 seconds|  0.2835 seconds |
| 2 | 200 |  0.2289 seconds | 0.2862 seconds|
| 3 | 400 |  0.2274 seconds| 0.3635 seconds  |
| 4 | 800 |  0.2264 seconds |  0.4812 seconds |
| 5 | 1600 | 0.2292 seconds  |  0.7350 seconds|
| 6 | 3200 | 0.2320 seconds| 1.2296 seconds |
| 7 | 6400 | 0.2505 seconds | 2.2272 seconds |
| 8 | 12800 | 0.2890 seconds | 4.2251 seconds|

![imagen1](images/graficarangesearch.png)



## Pruebas Funcionales Range Search

Se implemento dos tipos de funciones para la busqueda Range , el primero es el Range-sequential y el segundo es el Range-Rtree. Ambas funciones se encuentran dentro del archivo search.py.

Por un lado, para  la busqueda Range-Rtree se va a cargar a disco el archivo Rtree_{size}.idx  con la ayuda de la libreria Rtree .Se va a crear un range vector llamado  `bounds` de tamano  256 que va a tener los valores limites de cada elemento de los vectores caracteristicos que se buscan.  Se va a llamar al metodo `intersect` para encontrar a estos vectores que estan en el Rtree y se encuentrand de los limites de `bounds`, y luego en el archivo Sequential_{size}.json se va a obtener la direccion de las fotos resultantes.

Por otro lado , para la busqueda Range-Sequential se va a cargar a disco el archivo Sequential_{size}.json en bloques de 100 objetos . Esto para que no se agote la memoria. Luego se va verificar que los vectores esten dentro del range vector llamado `bounds` y se obtendra la direccion de las fotos resultantes. 


Para las pruebas funconales del Range Search, la variable r tomó el valor de 5 . Se hizo el testing para tamano de imagenes, luego se grafico los tiempos del Range tree y Range Sequential 

| Test  | Size  |Range - Rtree | Range - Secuencial| 
| :------------ |:---------------:| -----:| ------:|
| 1 | 100 |   0.2413 seconds|   0.3886 seconds |
| 2 | 200 | 0.2428 seconds  |	0.5486 seconds |
| 3 | 400 | 0.2677 seconds |   0.8184 seconds |
| 4 | 800 | 0.3065 seconds | 1.4662 seconds   |
| 5 | 1600 | 0.3912 seconds | 2.6174 seconds |
| 6 | 3200 | 0.5727 seconds | 4.8454 seconds|
| 7 | 6400 | 0.9018 seconds |9.5090 seconds |
| 8 | 12800 | 1.6106 seconds|19.3765 seconds |


![imagen1](images/graficaknnsearch.png)
