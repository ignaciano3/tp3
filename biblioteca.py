from grafo import Grafo
import random

class Cola:

    def __init__(self):
        self.cola = []

    def esta_vacia(self):
        return len(self.cola) == 0
        
    def encolar(self, item):
        self.cola.append(item)

    def ver_primero(self):
        return self.cola[0]

    def desencolar(self):
        if len(self.cola) < 1:
            return None
        return self.cola.pop(0)

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
        if camino[i] == destino: break
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


#Ciclo n por dfs
def reconstruir_ciclo(grafo : Grafo, v, destino, padres):
    print(grafo.info(destino), end = " --> ")

    while v is not destino:
        print(grafo.info(v), end = " --> ")
        v = padres[v]
    
    print(grafo.info(v))

def ciclo_dfs(grafo : Grafo, v, destino, n, visitados, padres):
    if n < 0: return False

    if n == 0 and destino in grafo.adyacentes(v): 
        reconstruir_ciclo(grafo, v, destino, padres)
        return True

    visitados.add(v)
    for w in grafo.adyacentes(v):
        if w not in visitados:
            padres[w] = v
            ciclo = ciclo_dfs(grafo, w, destino, n-1, visitados, padres)
            if ciclo: return True
    
    return False

def ciclo_n(grafo : Grafo, origen, n):

    for w in grafo.adyacentes(origen):
        visitados = set()
        padres = dict()
        padres[w] = origen
        visitados.add(origen)
        if ciclo_dfs(grafo, w, origen, n-2, visitados, padres): return
    print("No se encontro recorrido")


def pagerank_iterar(grafo: Grafo, pagerank_list : list()):
    d = 0.85
    for v in range (grafo.V):
        pagerank_vecinos = sum([pagerank_list[j] / len(grafo.adyacentes(j)) for j in grafo.adyacentes(v)])
        pagerank_list[v] = (1-d)/grafo.V + d * pagerank_vecinos

def pagerank(grafo : Grafo):
    pagerank_list = [1/grafo.V]* grafo.V
    while True:
        pagerank_iterar(grafo, pagerank_list)
        if (abs(sum(pagerank_list) - 1) < 0.0001): break
        # gracias a dios que no existe un #define en python
        # y no me pueden decir de los numeros magicos
    return pagerank_list



def pagerank_personalizado_iterar(grafo: Grafo, entrada : int, pagerank_list : list(), largo_viaje : int, valor: float):
    if (largo_viaje == 0): return 

    vecinos = grafo.adyacentes(entrada)
    salida = random.choice(vecinos)
    pagerank_list[salida] += valor/len(vecinos)
    pagerank_personalizado_iterar(grafo, salida, pagerank_list, largo_viaje-1, valor/len(vecinos))

def pagerank_personalizado(grafo: Grafo, seed: list()):
    pagerank_list = [0]* grafo.V
    for _ in range(1000):
        for s in seed:
            pagerank_personalizado_iterar(grafo, s, pagerank_list, largo_viaje = 5, valor = 1.)
            pagerank_list[s] = 0
    return pagerank_list