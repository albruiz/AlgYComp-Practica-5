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

    #random.seed(a = semilla, version = 2)
    for i in range(open):
        row,col = 0, 0
        #vert_horz = random.randint(0,1)       
        vert_horz = float(lfsr113(estado)) % 2
        
        if  vert_horz == 0 :
            #row = random.randint(0,size-1)
            #col = random.randint(0,size-2)
            row = lfsr113(estado) % (size)
            col = lfsr113(estado) % (size-1)
            
            row = row * 2 + 1
            col = col * 2 + 2 
        else:
            #row = random.randint(0,size-2)
            #col = random.randint(0,size-1)
            row = lfsr113(estado) % (size-1)
            col = lfsr113(estado) % (size)

            row = row * 2 + 2
            col = col * 2 + 1 
            
        #matriz[row][col] = random.randint(1,9)
        matriz[row][col] = float(lfsr113(estado2)) % 10


    # Escoge y marca habitación de salida
    #rowSal = random.randint(0, size-1)
    #colSal = random.randint(0, size-1)
    rowSal = (lfsr113(estado))  % size
    colSal = (lfsr113(estado))  % size

    xsalida,ysalida = rowSal*2+1, colSal*2+1
    matriz[xsalida][ysalida] = -1 

    # Escoge y marca habitación de destino
    #rowDes = random.randint(0, size-1)
    #colDes = random.randint(0, size-1)
    rowDes = (lfsr113(estado))  % size
    colDes = (lfsr113(estado))  % size

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
    while condicion == False:

        posiblesPuntos = getPuntos(matriz, final, matrizGrande)
        # recorrer posibles puntos para detectar puntos que ya se han recorrido y los eliminamos
        vectorInteremedio = []
        for i in range(len(posiblesPuntos)):
            if (posiblesPuntos[i] in coordenadasCamino) == False: 
                vectorInteremedio.append(posiblesPuntos[i])
        siguientePunto = getPuntoMinimo(matriz, vectorInteremedio)
        coordenadasCamino.append(siguientePunto)
        final = siguientePunto
        if siguientePunto == inicial: condicion = True
        else: pass


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
        if contador == (len(matriz) * 50): 
            print(contador)
            return 1 #limite por si no encuentra caminos
    pintaCaminoMejor(cola, puntoFinal, puntoInicial, matriz)
    return 0

# Funcion que busca dentro de la matriz los puntos sobre los que puede moverse para encontrar el camino menor
# realiza una busqueda entre los puntos adyacentes del punto introducido, si encuentra una pared no la anyade si encunetra una puerta
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
    habitaciones.append(puntoMatrizHabitaciones([x, y-2]))
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
    #Creacion de las colas, matrizBool se encargara de almacenar los puntos que se han mirado y servira para que 
    #cuando se encuentren las dos colas se sepa que son los puntos los que ya se han mirado y hay que determinar un camino optimo
    cola1 = np.array([numHabitaciones, numHabitaciones])
    cola2 = np.array([numHabitaciones, numHabitaciones])
    matrizBool = np.full((numHabitaciones,numHabitaciones), False)
    #obtengo las posiciones de los puntos para inicializarlos a 0
    inicio = puntoMatrizHabitaciones(puntoInicio)
    fin = puntoMatrizHabitaciones(puntoFin)
    cola1[inicio[0]][inicio[1]] = 0
    cola2[fin[0]][fin[1]] = 0

    condicion = False
    while condicion == False:
        puntos1, habitaciones1 = damePuntos(matriz, puntoInicio)
        puntos2, habitaciones2 = damePuntos(matriz, puntoFin)

        if matrizBool[inicio[0]][inicio[1]] == True: condicion = True
        else: matrizBool[inicio[0]][inicio[1]] = True
        if matrizBool[fin[0]][fin[1]] == True: condicion = True
        else: matrizBool[fin[0]][fin[1]] = True
        
        distanciaAuxiliar = math.inf
        puntoMenor1 = []
        contador = 0
        habitacion1 = []
        for i in puntos1:
            distance = matriz[i[0]][i[1]]
            if distance <= distanciaAuxiliar: 
                distanciaAuxiliar = distance
                puntoMenor1 = i
                habitacion1 = habitaciones1[contador]
            else: pass
            contador += 1
        
        distanciaAuxiliar = math.inf
        puntoMenor2 = []
        contador = 0
        habitacion2 = []
        for i  in puntos2:
            distance = matriz[i[0]][i[1]]
            if distance <= distanciaAuxiliar: 
                distanciaAuxiliar = distance
                puntoMenor2 = i
                habitacion2 = habitaciones2[contador]
            else: pass 
            contador += 1

        





#main
solucion = []
size = 20
ratio = 1
seed = 1312
seed2 = 1213
start_time = time()
solucion = generaLaberinto(size,ratio,seed, 1213)
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
    plot((puntoInicial[1])/(size*2+1), (len(matriz)- 1 - puntoInicial[0])/(size*2+1),  'sc')
    plot(puntoFinal[1]/(size*2+1), (len(matriz)- 1 - puntoFinal[0])/(size*2+1), 'sr')
    show()

