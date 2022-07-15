import random
from Cola import Cola
import numpy as np
from operator import truediv

from grafo import Grafo

# Camino mas corto
def camino_mas_corto_bfs(grafo : Grafo, origen, destino):
    visitados = set()
    visitados.add(origen)
    padres = dict()
    padres[origen] = None
    cola = Cola()
    cola.encolar(origen)
    
    while True:
        s = cola.desencolar()
        if s == destino:
            break

        for i in grafo.adyacentes(s):
            if i not in visitados:
                cola.encolar(i)
                visitados.add(i)
                padres[i] = s

        if cola.esta_vacia():
            print("No se encontro recorrido")
            return
    
    camino = list()
    while (s != None):
        camino.append(s)
        s = padres[s]
    camino.reverse()
    
    for i in range(0, len(camino), 2):
        # que horrible es la manera de representar el camino mas corto por dios
        # claro ejemplo no aclares que oscurece
        if (camino[i] == destino): break
        print(grafo.info(camino[i]), end= " --> ")
        print("aparece en playlist --> ", end ="")
        print(grafo.peso(camino[i], camino[i+1]), end = " --> ")
        print("de --> ", end="")
        print(grafo.info(camino[i+1]), end = " --> ")
        print("tiene una playlist", end =" --> ")
        print(grafo.peso(camino[i+1], camino[i+2]), end =" --> ")
        print("donde aparece --> ", end="") #que horrible todos estos: aparece... de... donde aparece... deberian sacarlos
        
    
    print(grafo.info(camino[i]))


# Todos en rango
def todos_en_rango(grafo : Grafo, origen, k):
    visitados = set()
    cola = Cola()
    orden = dict()
    orden[origen] = 0
    cola.encolar(origen)
    visitados.add(origen)
    
    en_rango= 0
    while not cola.esta_vacia():
        s = cola.desencolar()
        for i in grafo.adyacentes(s):
            if i not in visitados:
                cola.encolar(i)
                visitados.add(i)
                orden[i] = orden[s] + 1
                if orden[i] == k: en_rango += 1
                if orden[i] > k: break

    print(en_rango)
    return


#Ciclo n por dfs
def reconstruir_ciclo(grafo : Grafo, v, destino, padres):
    print(grafo.info(destino), end = " --> ")
    while v is not destino:
        print(grafo.info(v), end = " --> ")
        v = padres[v]
    print(grafo.info(destino))

    return

def ciclo_dfs(grafo : Grafo, v, destino, n, visitados, padres):
    if n < 0: return False

    if n == 0 and destino in grafo.adyacentes(v): 
        reconstruir_ciclo(grafo, v, destino, padres)
        return True

    visitados.add(v)
    for w in grafo.adyacentes(v):
        if w not in visitados and w is not destino:
            padres[w] = v
            ciclo = ciclo_dfs(grafo, w, destino, n-1, visitados, padres)
            if ciclo: return True
    
    return False

def ciclo_n(grafo : Grafo, origen, n):

    for w in grafo.adyacentes(origen):
        visitados = set()
        padres = dict()
        padres[w] = origen
        if ciclo_dfs(grafo, w, origen, n-2, visitados, padres): return
    print("No se encontro recorrido")

def matriz_adyacencia(grafo):
    M = np.zeros((grafo.V, grafo.V))
    for v in range(grafo.V):
        for w in grafo.adyacentes(v):
            M[w][v] = 1/len(grafo.adyacentes(v))
    return M

def pagerank(grafo : Grafo, num_iterations: int = 30, d: float = 0.85):
    # Deberia funcionar bien pero creo q el de grafo canciones esta mal
    # me tira tambien otros numeros para el todos en rango
    N = grafo.V
    v = np.ones(N) / N
    M = matriz_adyacencia(grafo)

    M_hat = (d * M + (1 - d) / N)
    for _ in range(num_iterations):
        v = v @ M_hat
    return v