# Alberto Ruiz - @albruiz
# Algoritmos y Computacion - UVa

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits import mplot3d
from pylab import *
from time import time

import random

# Funcion de estados aleatorios dada por Arturo
# Recibe por parametros el estado actual
def lfsr113(state):
    z1 = state[0]
    z2 = state[1]
    z3 = state[2]
    z4 = state[3]

    b = (((z1 << 6) ^ z1) >> 13)
    z1 = (((z1 & 4294967294) << 18) ^ b)

    b = (((z2 << 2) ^ z2) >> 27)
    z2 = (((z2 & 4294967288) << 2) ^ b)

    b = (((z3 << 13) ^ z3) >> 21)
    z3 = (((z3 & 4294967280) << 7) ^ b)

    b = (((z4 << 3) ^ z4) >> 12)
    z4 = (((z4 & 4294967168) << 13) ^ b)

    b = (z1 ^ z2 ^ z3 ^ z4)

    state[0] = z1
    state[1] = z2
    state[2] = z3
    state[3] = z4
    
    b = (b & 0xFFFFFFFF)

    return(b)

# Funcion de estados aleatorios dada por Arturo
# Recibe por parametros la semilla y el vector de estados
def lfsr113_seed(seed, state):
    z1 = 2
    z2 = 8
    z3 = 16
    z4 = 128

    z1 = (z1 * (seed + 1))
    z2 = (z2 * (seed + 1))
    z3 = (z3 * (seed + 1))
    z4 = (z4 * (seed + 1))

    z1 = z1 if (z1 > 1) else z1 + 1
    z2 = z2 if (z2 > 7) else z2 + 7
    z3 = z3 if (z3 > 15) else z3 + 15
    z4 = z4 if (z4 > 127) else z4 + 127

    state.append(z1)
    state.append(z2)
    state.append(z3)
    state.append(z4)

    return(state)


# Funcion que crea la matriz con las habitaciones y las paredes, ademas de dar el punto inicio y fin
# Recibe como parametros el tamaño de la matriz de habitaciones, el ratio de paredes que tiene que eliminar y la semilla de random
def generaLaberinto(size, ratio, semilla, semilla2):
    matriz_size = size*2+1
    matriz = np.zeros((matriz_size,matriz_size))
    # Rellena con habitación o pared
    for i in range(matriz_size):
        for j in range(matriz_size):
            if i % 2 == 1 and j % 2 == 1: matriz[i][j] = 0
            else: 
                matriz[i][j] = 10
    num_doors = 2 * (size-1) * (size-1)
    open = ratio * num_doors
    # Quita paredes

    estado = []
    estado = lfsr113_seed(semilla, estado)
    estado2 = []
    estado2 = lfsr113_seed(semilla2, estado2)

    for i in range(open):
        row,col = 0, 0
        vert_horz = float(lfsr113(estado)) % 2
        
        if  vert_horz == 0 :
            row = lfsr113(estado) % (size)
            col = lfsr113(estado) % (size-1)
            
            row = row * 2 + 1
            col = col * 2 + 2 
        else:
            row = lfsr113(estado) % (size-1)
            col = lfsr113(estado) % (size)

            row = row * 2 + 2
            col = col * 2 + 1 
        matriz[row][col] = float(lfsr113(estado2)) % 10


    # Escoge y marca habitación de salida
    rowSal = (lfsr113(estado))  % size
    colSal = (lfsr113(estado))  % size

    xsalida,ysalida = rowSal*2+1, colSal*2+1
    matriz[xsalida][ysalida] = -1 

    # Escoge y marca habitación de destino
    rowDes = (lfsr113(estado))  % size
    colDes = (lfsr113(estado))  % size

    xentrada, yentrada =  rowDes*2+1, colDes*2+1
    matriz[xentrada][yentrada] = -2 
    solucion = [matriz, [xsalida,ysalida], [xentrada, yentrada]] # devuelve la matriz llena de valores, el punto de salida y el destino
    return solucion


# Funcion que devuelve los puntos sobre los que podrá elegir el menor para dibujar el camino
# solucion
# Recibe por parametros la matriz de habitaciones y el punto sobre el que tiene que buscar los adyacentes
def getPuntos(matriz, punto, matrizGrande):
    # punto X, Y
    x, y = punto[0], punto[1]
    posiblesPuntos = [] # aqui almacenaremos los posibles puntos sobre los que podra avanzar

    # se bucan cuatro puntos respectivamente
    # punto con una variacion de -1 en las coordenadas de las X
    if x - 1 >= 0:
        puntoIntermedio = puntoReal([x-1, y])
        puntoIntermedio[0] += 1
        if matrizGrande[puntoIntermedio[0]][puntoIntermedio[1]] != 10:
            posiblesPuntos.append([x-1, y])
        else: pass
    else: pass

    # punto con una variacion de +1 en las coordenadas de las X
    if x + 1 <= (len(matriz) - 1):
        puntoIntermedio = puntoReal([x + 1, y])
        puntoIntermedio[0] -= 1
        if matrizGrande[puntoIntermedio[0]][puntoIntermedio[1]] != 10:
            posiblesPuntos.append([x+1, y])
        else: pass
    else: pass

    # punto con una variacion de -1 en las coordenadas de las Y
    if y - 1 >= 0:
        puntoIntermedio = puntoReal([x, y - 1])
        puntoIntermedio[1] += 1
        if matrizGrande[puntoIntermedio[0]][puntoIntermedio[1]] != 10:
            posiblesPuntos.append([x, y - 1])
        else: pass
    else: pass

    # punto con una variacion de +1 en las coordenadas de las Y
    if y + 1 <= (len(matriz) - 1):
        puntoIntermedio = puntoReal([x, y + 1])
        puntoIntermedio[1] -= 1
        if matrizGrande[puntoIntermedio[0]][puntoIntermedio[1]] != 10:
            posiblesPuntos.append([x, y+1])
        else: pass
    else: pass

    # en el caso de usar una cola cuyos valores son numeros e infinitos para designar aquellas habitaciones sobre las que  no puede acceder
    # puntosFinales almacenara los puntos sobre los que se puede avanzar que no tengan un valor de infinito
    # en los casos de usar una cola llena de None como es mi caso no es necesario añadir estas lineas, aunque nunca les resultara fallo
    puntosFinales = []
    for i in range(len(posiblesPuntos)):
        if matriz[posiblesPuntos[i][0]][posiblesPuntos[i][1]] != math.inf:
            puntosFinales.append(posiblesPuntos[i])
        else: pass

    #posiblesPuntos Es el vector de los puntos que tienen valores menores de infinito
    return puntosFinales


# Funcion que devuelve las coordenadas del punto que menor distancia acumulada tenga de los que tenga el vector
# Recibe por parametros la matriz que tendrá almacenada las distancias y el Vector con los puntos posibles
def getPuntoMinimo(matriz, vectorPuntos):
    puntoMinimo = []
    minimo = math.inf
    # el que tenga menor distancia acumukada sera el elegido, puede cambiar si hay valores menores que no han sido evaluados dentro del vector
    for i in vectorPuntos: 
        if matriz[i[0]][i[1]] != None and matriz[i[0]][i[1]] <= minimo:
            minimo = matriz[i[0]][i[1]]
            puntoMinimo = i
        else: pass
    return puntoMinimo


# Funcion que dibuja el mejor camino dentro de todos los caminos observados, elige partiendo del nodo destino, el menor peso con sus vecinos
# asi recursivamente hasta que alcanza el punto inicial y para de buscar porque ya tendra el camino solucion
# Recibe como argumentos, la matriz de las habitaciones con los costes para llegar del nodo inicio al nodo fin ya calculados
def pintaCaminoMejor(matriz, puntoFin, puntoInicio, matrizGrande):
    coordenadasCamino = []
    final = puntoMatrizHabitaciones(puntoFin)
    coordenadasCamino.append(final)
    inicial = puntoMatrizHabitaciones(puntoInicio)
    
    # final = punto del que se parte 
    # inicial = punto al que hay que llegar
    condicion = False
    while condicion == False:

        posiblesPuntos = getPuntos(matriz, final, matrizGrande)
        # recorrer posibles puntos para detectar puntos que ya se han recorrido y los eliminamos
        vectorIntermedio = []
        for i in range(len(posiblesPuntos)):
            if (posiblesPuntos[i] in coordenadasCamino) == False: 
                vectorIntermedio.append(posiblesPuntos[i])
        siguientePunto = getPuntoMinimo(matriz, vectorIntermedio)
        coordenadasCamino.append(siguientePunto) # voy anyadiendo los puntos que formaran el camino
        final = siguientePunto
        if siguientePunto == inicial: condicion = True
        else: pass

    # aqui es donde se pinta el camino resultante, se hace como lo hemos ido haciendo con la libreria plot de python
    for i in coordenadasCamino:
        aux = puntoReal(i)
        plot(aux[1]/len(matrizGrande), (len(matrizGrande) -1 - aux[0])/len(matrizGrande), 'Hm')


# Funcion que dibuja la matriz con su punto de inicio, punto de fin y el laberinto
# toma como argumentos, la matriz, el punto de inicio, el punto de fin y el tamano de la matriz
def dibujamela(matriz,puntoInicio, puntoFin, tamano):
    tamano = tamano*2 +1
    paredesX, paredesY = [],[]
    puertasX, puertasY = [],[]
    x, y = 0,0
    contador2 = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 10: # aqui se encargara de pintar las paredes 
                paredesX.append((len(matriz)- 1 - i)/(tamano))
                paredesY.append((j)/(tamano))
                x+=1
                contador2 += 1
            else:  #if matriz[i][j] == 0: 
                # se encargara de pintar las habitaciones
                puertasX.append((len(matriz)- 1 -i)/(tamano))
                puertasY.append((j)/(tamano))
                y+=1
    # usamos la librerio plot de python 
    plot(paredesY, paredesX, 'sk')
    plot(puertasY, puertasX, 'sy')


# Funcion que devuelve las coordenadas de un punto de la matriz grande, donde hay habitaciones y paredes en coordenadas de 
# la matriz que solo almacena habitaciones.
# Recibe como parametro el punto de la matriz grande que debera transformar
def puntoMatrizHabitaciones(punto):
    nuevasCoordenadas = [int((punto[0] - 1)/2), int((punto[1] - 1)/2)]
    return nuevasCoordenadas


# Funcion que devuelve las coordenadas correctas sobre la matriz grande, tomando 
# como entrada un punto de la matriz de habitaciones (10,10)
def puntoReal(punto):
    nuevasCoordeanas = [(punto[0]*2) + 1, (punto[1]*2) + 1]
    return nuevasCoordeanas


# Funcion que busca dentro de la matriz los puntos sobre los que puede moverse para encontrar el camino menor
# realiza una busqueda entre los puntos adyacentes del punto introducido, si encuentra una pared no la anyade solo ayade los puntos que pueden ser caminos
# la almacena y ya sera el algortimo de Djiskstra quien se encargue de decidir si los puntos son buenos o no.
# Recibe por parametros la matriz con los valores que sera de donde obtenga la informacion y el punto sobre el que buscara los adyacentes.
def damePuntos(matriz, punto):
    puntos, vector, habitaciones, vectorHabitaciones = [],[],[],[]
    x,y = punto[0], punto[1]

    #Todos los puntos posibles sobre los que se debera mirar
    puntos.append([x-1, y])
    habitaciones.append(puntoMatrizHabitaciones([x-2, y]))
    puntos.append([x+1, y])
    habitaciones.append(puntoMatrizHabitaciones([x+2, y]))
    puntos.append([x, y-1])
    habitaciones.append(puntoMatrizHabitaciones([x, y-2]))
    puntos.append([x, y+1])
    habitaciones.append(puntoMatrizHabitaciones([x, y+2]))
    contador = 0
    for i in puntos:
        if matriz[i[0]][i[1]] != 10: 
            vector.append(i) # en el caso de que no sea una pared se almacenara
            vectorHabitaciones.append(habitaciones[contador])
        else: pass
        contador += 1
    return vector, vectorHabitaciones # es el vector con todos los puntos posibles


# Funcion que se encarga de devolver el calculo de la heuristia, es decir la distancia Manhattan entre
# los dos puntos que se le han pasado por parametros uno de ellos es el puntoInicio y otro de ellos
# es el puntoFin, la heuristica se calcula como la diferencia entre las coordenadas entre los puntos
def heuristica(puntoInicio, puntoFin):
    varX = abs(puntoInicio[0] - puntoFin[0])
    varY = abs(puntoInicio[1] - puntoFin[1])
    diferencia = varX + varY
    return diferencia


# Funcion que se encarga de calcular el camino minimo siguiendo las indicaciones del algoritmo a_estrella, en este caso deberemos tener en cuenta
# no solo la distancia tentativa entre los puntos sino que tambien habra que tener en cuenta el calculo de la distancia Mamhattan entre los puntos
# y el punto final, usamos la funcion f(n) = d(n) + h(n), donde d(n) = distancia tentativa y h(n) = heuristica de n
# como hemos seguido haciendo como queremos obtener el camino menor se elegira como siguiente punto el que menor valor tenga almacenado, f(n)
# Recibe por parametros la matriz de pesos, un puntoInicio, que sera el primero por el que empiece a buscar y un puntoFin que sera el punto
# destino; es decir el punto que hay que alcanzar; ademas del numero de habitaciones que hay en la matriz para poder inicializar la cola
def a_estrella(matriz, puntoInicio, puntoFin, numHabitaciones):

    # Definimos la cola que almacenara en este caso los calculos de la funcion dada
    # Diferenciandose así respecto a la anterior cola que solo almacenaba las distancias
    # tentativas, para almacenar el calculo ademas de usar una cola, usaremos una funcion
    # que se encargue de calcular los valores y almacenarlos en la cola.
    cola = np.full((numHabitaciones, numHabitaciones), None)
    matrizBool = np.full((numHabitaciones, numHabitaciones), False)
    inicio = puntoMatrizHabitaciones(puntoInicio)
    fin = puntoMatrizHabitaciones(puntoFin)
    puntoInicialReal = puntoInicio
    # le damos el valor a los puntos inicio
    cola[inicio[0]][inicio[1]] = 0
    
    contadorFinal = 0 #s ervira para salir de la funcion si no ha encontrado el camino
    resultado = 0 # se usara para saber si ha habido un resultado correcto o no
    condicion = False

    # con este bucle encontramos el mejor camino usando la nueva heuristica
    while condicion == False:
        matrizBool[inicio[0]][inicio[1]] = True
        p, h = damePuntos(matriz, puntoInicio)

        # Este bucle nos permite rellenar la cola con los valores de la funcion, unicamente 
        # da valores en la matriz, a los puntos que pueden ser usados como habitaciones
        # puente, es decir habitaciones por las que se puede pasar.
        habitaciones = []
        puntos = []
        contador = 0
        for i in h:
            if matrizBool[i[0]][i[1]] == False:
                punto = p[contador]
                suma = cola[inicio[0]][inicio[1]] + matriz[punto[0]][punto[1]] + heuristica(i, fin)
                if cola[i[0]][i[1]] == None:
                    cola[i[0]][i[1]] = suma
                    puntos.append(p[contador])
                    habitaciones.append(i)
                elif cola[i[0]][i[1]] > suma:
                    cola[i[0]][i[1]] = suma
                    puntos.append(p[contador])
                    habitaciones.append(i)
                else: pass
            else: pass
            contador += 1

        # Uso este bucle para encontrar el menor valor de todos los que tengo
        # y ese sera el punto sobre el que pivotemos hasta alcanzar el ultimo punto
        min = math.inf
        pmin = []
        for i in range(len(cola)):
            for j in range(len(cola)):
                if cola[i][j] != None:
                    if matrizBool[i][j] != True and cola[i][j] <= min:
                        min = cola[i][j]
                        pmin = [i,j]
                    else: pass
                else: pass

        # en el caso de que el punto minimo sea vacio, significara que no puede avanzar y por lo tanto no hay camino 
        # para alcanzar el punto final, se terminara
        if pmin == []: 
            resultado = 1 # resultado que indica que no hay camino, se sale del bucle
            condicion = True
            break
        else: pass

        # En el caso de que el punto con menor valor para la funcion sea el puntoFin
        # se habra encontrado el menor camino y se podra terminar
        # En caso contrario se dan valores nuevos a las variables que indican el puntoInicial
        # estos valores serar los valores del punto minimo
        if pmin == fin:
            resultado = 0 #resultado correcto
            condicion = True
        else:
            inicio = pmin
            puntoInicio = puntoReal(inicio)


        contadorFinal += 1
        if contadorFinal == (np.size(cola)*10): # en el caso de que el bucle no termine, le anyadimos un limite para que muestre el error
            resultado = 1 # lo usaremos para lanzar un mensaje de error
            condicion = True # condicion de salida por si no existe un camino

    # una vez se han encontrado vamos a dibujar el camino
    if resultado == 0:
        pintaCaminoMejor(cola, puntoFin, puntoInicialReal, matriz)
        return resultado
    else:
        return resultado

  



#################### MAIN
solucion = []
size = 20
ratio = 1
seed = 1234
seed2 = 1357
start_time = time() # comenzamos a contar el tiempo
solucion = generaLaberinto(size,ratio,seed, 1213) # se genera el laberinto
matriz = solucion[0] # matriz de valores
puntoInicial = solucion[1] # punto inicial
puntoFinal = solucion[2] # punto final
numeroHabitaciones = size # numero de habitaciones

dibujamela(solucion[0],solucion[1], solucion[2], size) # dibujar la matriz sin el camino

valor = a_estrella(matriz, puntoInicial, puntoFinal, numeroHabitaciones) # calcular el camino mejor y dibujar el mejor camino


# en el caso de que el resultado sea el correcto valor sera igual a 0 y por lo tanto pintara el camino bueno e imprimira el tiempo
if valor == 0: 
    plot((puntoInicial[1])/(size*2+1), (len(matriz)- 1 - puntoInicial[0])/(size*2+1),  'sc')
    plot(puntoFinal[1]/(size*2+1), (len(matriz)- 1 - puntoFinal[0])/(size*2+1), 'sr')
    show()
    elapsed_time = time() - start_time
    print("El programa tarda en ejecutarse %.10f" %elapsed_time, "segundos")
else: # en el caso de fallo, comenta el fallo y pinta la matriz sin el camino con el tiempo de ejecucion
    print("No hay soluciones posibles")
    elapsed_time = time() - start_time
    print("El programa tarda en ejecutarse %.10f" %elapsed_time, "segundos")
    plot((puntoInicial[1])/(size*2+1), (len(matriz)- 1 - puntoInicial[0])/(size*2+1),  'sc')
    plot(puntoFinal[1]/(size*2+1), (len(matriz)- 1 - puntoFinal[0])/(size*2+1), 'sr')
    show()

