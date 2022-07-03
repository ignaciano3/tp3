from Cola import Cola
from Pila import Pila

class Grafo:

    def __init__(self, vertices, dirigido = False):
        self.V = vertices
        self.directed = dirigido
        self.graph = dict()

        for i in range(self.V):
            self.graph[i] = dict()
    
    def add_edge(self, src, dest, peso = 1):
        self.graph[src][dest] = peso
        if not self.directed:
            self.graph[dest][src] = peso
    
    def peso(self, src, dest):
        return self.graph[src][dest]
    
    def adyacentes(self, v):
        ady = list()
        for i in self.graph[v].keys():
            ady.append(i)
        ady.sort()
        return ady

    def camino_mas_corto_bfs(self, origen, destino):
        visitados = set()
        padres = dict()
        padres[origen] = -1
        cola = Cola()
        cola.encolar(origen)
        
        while not cola.esta_vacia():
            s = cola.desencolar()
            if (s == destino): break
            for i in self.adyacentes(s):
                if i not in visitados:
                    cola.encolar(i)
                    visitados.add(i)
                    padres[i] = s

        pila = Pila()
        pila.apilar(s)
        while (padres[s] != origen):
            pila.apilar(padres[s])
            s = padres[s]

        print(f"{origen}", end =" ")

        while not pila.esta_vacia():
            p = pila.desapilar()
            print(f">>> {p}", end=" ")

    def todos_en_rango(self, origen, k):
        visitados = set()
        cola = Cola()
        orden = dict()
        orden[origen] = 0
        cola.encolar(origen)

        en_rango= 0
        while not cola.esta_vacia():
            s = cola.desencolar()
            for i in self.adyacentes(s):
                if i not in visitados:
                    cola.encolar(i)
                    visitados.add(i)
                    orden[i] = orden[s] + 1
                    if (orden[i] == k): en_rango += 1
                    if (orden[i] > k): break

        return en_rango


class Grafo_con_datos(Grafo):
    
    def __init__(self, vertices, data, dirigido=False):
        super().__init__(vertices, dirigido)
        self.data = dict()
        for i in range (self.V):
            self.data[i] = data[i]
    
    def info(self, v):
        return self.data[v]