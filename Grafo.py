from Cola import Cola

class Grafo:

    def __init__(self, vertices, data, dirigido = False):
        self.V = vertices
        self.directed = dirigido
        self.graph = dict()
        self.data = dict()

        for i in range(self.V):
            self.graph[i] = dict()
            self.data[i] = data[i]
    

    def add_edge(self, src, dest, peso = 1):
        self.graph[src][dest] = peso
        if not self.directed:
            self.graph[dest][src] = peso
    
    def peso(self, src, dest):
        return self.graph[src][dest]
    
    def info(self, v):
        return self.data[v]

    def adyacentes(self, v):
        ady = list()
        for i in self.graph[v].keys():
            ady.append(i)
        return ady

    def printear(camino):
        pass

    def camino_mas_corto_bfs(self, origen, destino):
        visitados = set()
        visitados.add(origen)
        padres = dict()
        padres[origen] = None
        cola = Cola()
        cola.encolar(origen)
        
        while True:
            s = cola.desencolar()
            if (s == destino):
                break

            for i in self.adyacentes(s):
                if i not in visitados:
                    cola.encolar(i)
                    visitados.add(i)
                    padres[i] = s

            if(cola.esta_vacia()):
                print("No se encontro recorrido")
                return
        
        camino = list()
        while (s != None):
            camino.append(self.info(s))
            s = padres[s]
        camino.reverse()
        
        for x in camino:
            if (x == self.info(destino)): break
            print(x, end= " >>>> ")
        
        print(x)

    
    def todos_en_rango(self, origen, k):
        visitados = set()
        cola = Cola()
        orden = dict()
        orden[origen] = 0
        cola.encolar(origen)
        visitados.add(origen)
        
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

        print(en_rango)
        return
    
    def reconstruir_ciclo(self, v, destino, padres):
        print(self.info(destino), end = " --> ")
        while v is not destino:
            print(self.info(v), end = " --> ")
            v = padres[v]
        print(self.info(destino))

        return


    def ciclo_dfs(self, v, destino, n, visitados, padres):
        if n < 0: return False

        if n == 0 and destino in self.adyacentes(v): 
            self.reconstruir_ciclo(v, destino, padres)
            return True

        visitados.add(v)
        for w in self.adyacentes(v):
            if w not in visitados and w is not destino:
                padres[w] = v
                ciclo = self.ciclo_dfs(w, destino, n-1, visitados, padres)
                if ciclo: return True
        
        return False


    def ciclo_n_canciones(self, origen, n):

        for w in self.adyacentes(origen):
            visitados = set()
            padres = dict()
            padres[w] = origen
            if self.ciclo_dfs(w, origen, n-2, visitados, padres): return
        print("No se encontro recorrido")