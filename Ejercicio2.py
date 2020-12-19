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
    #print(punto)
    nuevasCoordenadas = [int((punto[0] - 1)/2), int((punto[1] - 1)/2)]
    return nuevasCoordenadas


# Funcion que devuelve las coordenadas correctas sobre la matriz grande, tomando 
# como entrada un punto de la matriz de habitaciones (10,10)
def puntoReal(punto):
    nuevasCoordeanas = [(punto[0]*2) + 1, (punto[1]*2) + 1]
    return nuevasCoordeanas


# Funcion que devuelve los pesos acumulados
# Recibe como parametros el peso de la matriz, y el peso acumulado
def calculaPeso(peso, pesoAcumulado):
    if peso == 10 : 
        return math.inf
    else:
        return (pesoAcumulado + peso)


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


# Funcion que encunetra el camino mas corto haciendo un recorrido a la vez desde el PuntoInicial y el PuntoFin
# Recibe como parametros la matriz de puntos, el puntoInicio desde el que se empieza a bucar, el PuntoFin que es el punto destino, aunque esta vez sera otro nodo inicial
# y el numero de habitaciones que nos servira para poder construir las 2 colas
def djikstraBidireccional(matriz, puntoInicio, puntoFin, numHabitaciones):
    # Creacion de las colas, matrizBool se encargara de almacenar los puntos que se han mirado y servira para que 
    # cuando se encuentren las dos colas se sepa que son los puntos los que ya se han mirado y hay que determinar un camino optimo
    cola1 = np.full((numHabitaciones, numHabitaciones), None)
    cola2 = np.full((numHabitaciones, numHabitaciones), None)
    matrizBool1 = np.full((numHabitaciones,numHabitaciones), False)
    matrizBool2 = np.full((numHabitaciones, numHabitaciones), False)
    # obtengo las posiciones de los puntos para inicializarlos a 0
    puntoInicialReal = puntoInicio #usaremos estas dos variables posteriormente para poder pintar sin haber cambiado los valores originales
    puntoFinalReal = puntoFin
    puntoIntermedioReal = []
    inicio = puntoMatrizHabitaciones(puntoInicio)
    fin = puntoMatrizHabitaciones(puntoFin)
    # inicializamos los valores de los puntos inicio de las dos colas a 0, que seran de donde empezaremos a buscar en los dos casos
    cola1[inicio[0]][inicio[1]] = 0
    cola2[fin[0]][fin[1]] = 0

    resultado = 0 # servira para al final indicar si se ha encontrado un camino o no; 0 -> SI, 1 -> NO
    contadorFinal = 0 # limitador por si hay un fallo
    condicion = False
    while condicion == False:

        p1, h1 = damePuntos(matriz, puntoInicio) # puntos y habitaciones sobre los que se puede avanzar respecto a la cola1 y el punto de inicio
        p2, h2 = damePuntos(matriz, puntoFin) # puntos y habitaciones sobre los que se puede avanzar respecto a la cola2 y el punto de inicio(fin)
        # como los dos puntos sobre los que buscamos son los pivotes se les da valor de True en la matriz Booleana (cada uno en la suya)
        matrizBool1[inicio[0]][inicio[1]] = True 
        matrizBool2[fin[0]][fin[1]] = True

        # Con este bucle estamos llenando la cola con los valores de las distancias que se usaran para comparar
        # y decidir cual sera el punto desde el que seguiremos buscando el camino
        habitaciones1 = []
        puntos1 = []
        contador = 0
        for i in h1:
            if matrizBool1[i[0]][i[1]] == False:
                punto = p1[contador]
                suma = cola1[inicio[0]][inicio[1]] + matriz[punto[0]][punto[1]]
                if cola1[i[0]][i[1]] == None:
                    cola1[i[0]][i[1]] = suma
                    puntos1.append(p1[contador])
                    habitaciones1.append(i)
                elif cola1[i[0]][i[1]] > suma:
                    cola1[i[0]][i[1]] = suma
                    puntos1.append(p1[contador])
                    habitaciones1.append(i)
                else: pass
            else: pass
            contador += 1

        # Repetimos el bucle de arriba pero este caso es para la cola2, o la cola de los puntos que empiezan por el final
        habitaciones2 = []
        puntos2 = []
        contador = 0
        for i in h2:
            if matrizBool2[i[0]][i[1]] == False:
                punto = p2[contador]
                suma = cola2[fin[0]][fin[1]] + matriz[punto[0]][punto[1]]
                if cola2[i[0]][i[1]] == None:
                    cola2[i[0]][i[1]] = suma
                    puntos2.append(p2[contador])
                    habitaciones2.append(i)
                elif cola2[i[0]][i[1]] > suma:
                    cola2[i[0]][i[1]] = suma
                    puntos2.append(p2[contador])
                    habitaciones2.append(i)
                else: pass
            else: pass
            contador += 1
        
        # Buscamos el valor minimo en ambos casos para continuar buscando los elementos del camino
        min1 = math.inf
        min2 = math.inf
        pmin1 = []
        pmin2 = []
        # en pmin1 y pmin2 se almacenan las habitaciones sobre las que se buscara el resto 
        for i in range(len(cola1)):
            for j in range(len(cola1)):
                if cola1[i][j] != None: # se obtendra el punto minimo de la cola1
                    if matrizBool1[i][j] != True and cola1[i][j] <= min1:
                        min1 = cola1[i][j]
                        pmin1 = [i,j]
                    else: pass
                else: pass

                if cola2[i][j] != None: # se obtendra el punto minimo de la cola2
                    if matrizBool2[i][j] != True and cola2[i][j] <= min2:
                        min2 = cola2[i][j]
                        pmin2 = [i,j]
                    else: pass
                else: pass      

        # en el caso de que un valor minimo bo tenga coordenadas significara que no tiene camino y terminara la busqueda
        if pmin1 == [] or pmin2 == []:
            resultado = 1
            condicion = True
            break
        else: pass

        # se hace la comprobacion para saber si hemos encontrado ya el punto que une ambos caminos
        # en ese caso se termina la busqueda sino se dan valores nuevos a puntoInicio y puntoFin, con los valores
        # de los puntos minimos de cada busqueda y se continua
        if cola2[pmin1[0]][pmin1[1]] != None: 
            puntoIntermedioReal = puntoReal(pmin1)
            resultado = 0 # resultado correcto
            condicion = True # fin del bucle
        elif cola1[pmin2[0]][pmin2[1]] != None:
            puntoIntermedioReal = puntoReal(pmin2)
            resultado = 0 # resultado correcto
            condicion = True # fin del bucle
        else: 
            # nuevos valores
            inicio, fin = pmin1, pmin2 
            puntoInicio = puntoReal(inicio)
            puntoFin = puntoReal(fin)
        
        contadorFinal += 1 # en el caso de que no haya camino solucion y el algoritmo cotinue buscando sale con un limitador que he definido aqui
        if contadorFinal == (np.size(cola1)*10): 
            resultado = 1 # lo usaremos para lanzar un mensaje de error
            condicion = True # condicion de salida por si no existe un camino

    # una vez se han encontrado vamos a dibujar el camino
    if resultado == 0:
        pintaCaminoMejor(cola1, puntoIntermedioReal, puntoInicialReal, matriz) # primera parte del camino
        pintaCaminoMejor(cola2, puntoIntermedioReal, puntoFinalReal, matriz) # segunda parte del camino
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
valor = djikstraBidireccional(matriz, puntoInicial, puntoFinal, numeroHabitaciones) # calcular el camino mejor y dibujar el mejor camino

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

