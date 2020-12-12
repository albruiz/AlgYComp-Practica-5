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


# Funcion que crea la matriz con las habitaciones y las paredes, ademas de dar el punto inicio y fin
# Recibe como parametros el tamaño de la matriz de habitaciones, el ratio de paredes que tiene que eliminar y la semilla de random
def generaLaberinto(size, ratio, semilla):
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
    random.seed(a = semilla, version = 2)
    for i in range(open):
        row,col = 0, 0
        vert_horz = random.randint(0,1)       
        if  vert_horz == 0 :
            row = random.randint(0,size-1)
            col = random.randint(0,size-2)
            
            row = row * 2 + 1
            col = col * 2 + 2 
        else:
            row = random.randint(0,size-2)
            col = random.randint(0,size-1)
            
            row = row * 2 + 2
            col = col * 2 + 1 
            
        matriz[row][col] = random.randint(1,9)

    # Escoge y marca habitación de salida
    rowSal = random.randint(0, size-1)
    colSal = random.randint(0, size-1)
    
    xsalida,ysalida = rowSal*2+1, colSal*2+1
    matriz[xsalida][ysalida] = -1 

    # Escoge y marca habitación de destino
    rowDes = random.randint(0, size-1)
    colDes = random.randint(0, size-1)
    xentrada, yentrada =  rowDes*2+1, colDes*2+1
    matriz[xentrada][yentrada] = -2 
    solucion = [matriz, [xsalida,ysalida], [xentrada, yentrada]]
    return solucion


# Funcion que devuelve los puntos sobre los que podrá elegir el menor para dibujar el camino
# solucion
# Recibe por parametros la matriz de habitaciones y el punto sobre el que tiene que buscar los adyacentes
def getPuntos(matriz, punto, matrizGrande):
    # punto X, Y
    x, y = punto[0], punto[1]
    posiblesPuntos = []
    if x - 1 >= 0:
        puntoIntermedio = puntoReal([x-1, y])
        puntoIntermedio[0] += 1
        if matrizGrande[puntoIntermedio[0]][puntoIntermedio[1]] != 10:
            posiblesPuntos.append([x-1, y])
        else: pass
    else: pass

    if x + 1 <= (len(matriz) - 1):
        puntoIntermedio = puntoReal([x + 1, y])
        puntoIntermedio[0] -= 1
        if matrizGrande[puntoIntermedio[0]][puntoIntermedio[1]] != 10:
            posiblesPuntos.append([x+1, y])
        else: pass
    else: pass

    if y - 1 >= 0:
        puntoIntermedio = puntoReal([x, y - 1])
        puntoIntermedio[0] += 1
        if matrizGrande[puntoIntermedio[0]][puntoIntermedio[1]] != 10:
            posiblesPuntos.append([x, y - 1])
        else: pass
    else: pass

    if y + 1 <= (len(matriz) - 1):
        puntoIntermedio = puntoReal([x, y + 1])
        puntoIntermedio[1] -= 1
        if matrizGrande[puntoIntermedio[0]][puntoIntermedio[1]] != 10:
            posiblesPuntos.append([x, y+1])
        else: pass
    else: pass
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
    for i in vectorPuntos:
        if matriz[i[0]][i[1]] <= minimo:
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
    # final = punto del que se parte, inicial = punto al que hay que llegar
    condicion = False
    contador = 0
    while condicion == False:

        posiblesPuntos = getPuntos(matriz, final, matrizGrande)
        siguientePunto = getPuntoMinimo(matriz, posiblesPuntos)
        coordenadasCamino.append(siguientePunto)
        final = siguientePunto
        if siguientePunto == inicial: condicion = True
        else: pass
        contador += 1
        if contador == 10 :  condicion = True

    coordenadasCamino.pop(0)
    coordenadasCamino.pop(len(coordenadasCamino) - 1)
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
            if matriz[i][j] == 10: 
                paredesX.append((len(matriz)- 1 - i)/(tamano))
                paredesY.append((j)/(tamano))
                x+=1
                contador2 += 1
            else:  #if matriz[i][j] == 0: 
                puertasX.append((len(matriz)- 1 -i)/(tamano))
                puertasY.append((j)/(tamano))
                y+=1
    
    plot(paredesY, paredesX, 'sk')
    plot(puertasY, puertasX, 'sy')


# Funcion de devuelve los puntos que puede tomar el camino a seguir, es decir que no son puertas
# Recibe como argumentos, la matriz y el punto inicial
def puntosAdyacentes(matriz, puntoInicial):
    posicionX = puntoInicial[0]
    posicionY = puntoInicial[1]
    puntosIntermedios = []
    for i in range(2):
        if matriz[posicionX - 1][posicionY - 1 + i] < 10:
            puntosIntermedios.append([posicionX-1, posicionY - 1 + i])
        if matriz[posicionX + 1][posicionY - 1 + i] < 10:
            puntosIntermedios.append([posicionX-1, posicionY - 1 + i])
        if i != 1 and matriz[posicionX][posicionY - 1 + i] < 10:
            puntosIntermedios.append([posicionX, posicionY - 1 + i])
    return puntosIntermedios

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
# Funcion que devuelve los pesos acumulados
# Recibe como parametros el peso de la matriz, y el peso acumulado
def calculaPeso(peso, pesoAcumulado):
    if peso == 10 : 
        return math.inf
    else:
        return (pesoAcumulado + peso)

# Funcion que crea los caminos sobre los que se puede ir desde el punto inicio al punto final, usa una cola que almacena todas las distancias que hay entre puntos
# que pueden llegar a conectar el punto inicio y el punto fin
# Recibe como parametros la matriz inicial, el punto incial, el punto final y el numero de habitaciones que hay
def djikstra(matriz, puntoInicial, puntoFinal, numHabitaciones):
    # Cola = almacena el costo de ir a cada una de las puertas (peso acumulado)
    comprobacion = np.full((numHabitaciones,numHabitaciones), False)
    cola = np.full((numHabitaciones,numHabitaciones), math.inf)
    posicionInicial = [(int)(puntoInicial[0]-1)/2 , (int)(puntoInicial[1]-1)/2]
    valorX, valorY = (int)(posicionInicial[0]), (int)(posicionInicial[1])
    cola[valorX][valorY] = 0
    contador = 0
    condicion = False
    while condicion == False:
        punto1, punto2, punto3, punto4 = [valorX - 1, valorY], [valorX + 1, valorY], [valorX, valorY - 1], [valorX, valorY + 1]
        comprobacion[valorX, valorY] = True
        contador += 1
        # Variantes de X
        if punto1[0] < numHabitaciones and punto1[1] < numHabitaciones and punto1[0] >= 0 and punto1[1] >= 0:
            punto1Grande = puntoReal(punto1)
            peso = matriz[punto1Grande[0] + 1][punto1Grande[1]]
            if calculaPeso(peso, cola[valorX][valorY]) < cola[punto1[0], punto1[1]]:
                cola[punto1[0], punto1[1]] = calculaPeso(peso, cola[valorX][valorY])
            else: pass

            if cola[punto1[0], punto1[1]] < math.inf:
                plot((punto1Grande[1]/len(matriz)), (len(matriz) - 1 - punto1Grande[0])/len(matriz), 'sb')
        
        if punto2[0] < numHabitaciones and punto2[1] < numHabitaciones and punto2[0] >= 0 and punto2[1] >= 0:
            punto2Grande = puntoReal(punto2)
            peso = matriz[punto2Grande[0] - 1][punto2Grande[1]]
            if calculaPeso(peso, cola[valorX][valorY]) < cola[punto2[0], punto2[1]]:
                cola[punto2[0], punto2[1]] = calculaPeso(peso, cola[valorX][valorY])
            else: pass 

            if cola[punto2[0], punto2[1]] < math.inf:
                plot((punto2Grande[1])/len(matriz),( len(matriz) - 1 - punto2Grande[0])/len(matriz), 'sb')

        # Variantes de Y
        if punto3[0] < numHabitaciones and punto3[1] < numHabitaciones and punto3[0] >= 0 and punto3[1] >= 0:
            punto3Grande = puntoReal(punto3)
            peso = matriz[punto3Grande[0]][punto3Grande[1] + 1]
            if calculaPeso(peso, cola[valorX][valorY]) < cola[punto3[0], punto3[1]]:
                cola[punto3[0], punto3[1]] = calculaPeso(peso, cola[valorX][valorY])
            else: pass

            if cola[punto3[0], punto3[1]] < math.inf:
                plot((punto3Grande[1])/len(matriz), (len(matriz) - 1 - punto3Grande[0])/len(matriz), 'sb') 
        
        if punto4[0] < numHabitaciones and punto4[1] < numHabitaciones and punto4[0] >= 0 and punto4[1] >= 0:
            punto4Grande = puntoReal(punto4)
            peso = matriz[punto4Grande[0]][punto4Grande[1] - 1]
            if calculaPeso(peso, cola[valorX][valorY]) < cola[punto4[0], punto4[1]]:
                cola[punto4[0], punto4[1]] = calculaPeso(peso, cola[valorX][valorY])
            else: pass

            if cola[punto4[0], punto4[1]] < math.inf:
                plot((punto4Grande[1])/len(matriz), (len(matriz) -1 - punto4Grande[0])/len(matriz), 'sb')     

        var1, var0 = -1, -1
        minimo = math.inf
        for i in range(len(cola)):
            for j in range(len(cola[i])):
                if minimo > cola[i][j] and cola[i][j] >= cola[valorX][valorY] and comprobacion[i][j] == False:
                    if i != valorX or j != valorY:
                        minimo = cola[i][j]
                        var1, var0 = i, j
                    else: pass
                else: pass
        valorX, valorY = var1, var0
                
        if puntoReal([valorX, valorY]) == puntoFinal:
            condicion = True
        else: 
            a = puntoReal([valorX, valorY])
            plot((a[1] )/len(matriz),(len(matriz) -1 - a[0])/len(matriz), 'sb')
        if contador == (len(matriz) * 50): return 1 #limite por si no encuentra caminos
    pintaCaminoMejor(cola, puntoFinal, puntoInicial, matriz)
    return 0




#main
solucion = []
size = 10
ratio = 1
seed = 7
start_time = time()
solucion = generaLaberinto(size,ratio,seed)
matriz = solucion[0]
puntoInicial = solucion[1]
puntoFinal = solucion[2]
numeroHabitaciones = size


dibujamela(solucion[0],solucion[1], solucion[2], size)
valor = djikstra(matriz, puntoInicial, puntoFinal, numeroHabitaciones)
if valor == 0:
    plot((puntoInicial[1])/(size*2+1), (len(matriz)- 1 - puntoInicial[0])/(size*2+1),  'sc')
    plot(puntoFinal[1]/(size*2+1), (len(matriz)- 1 - puntoFinal[0])/(size*2+1), 'sr')
    show()
    elapsed_time = time() - start_time
    print("El programa tarda en ejecutarse %.10f" %elapsed_time, "segundos")
else:
    print("No hay soluciones posibles")
    elapsed_time = time() - start_time
    print("El programa tarda en ejecutarse %.10f" %elapsed_time, "segundos")

