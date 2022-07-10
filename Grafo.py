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
                print(self.info(s))
                break

            for i in self.adyacentes(s):
                if i not in visitados:
                    cola.encolar(i)
                    visitados.add(i)
                    padres[i] = s

            if(cola.esta_vacia()):
                print("No se encontro recorrido")
                break
        
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


    def ciclo_n_canciones(self, origen, n):
        visitados = set()
        padres = dict()
        padres[origen] = None
        orden = dict()
        orden[origen] = 0
        cola = Cola()
        cola.encolar(origen)
        visitados.add(origen)
        
        while not cola.esta_vacia():
            s = cola.desencolar()
            if (orden[s] > n): return None
            if (orden[s] == n-2 and s in self.adyacentes(origen)): break
            
            for i in self.adyacentes(s):
                if i not in visitados:
                    cola.encolar(i)
                    visitados.add(i)
                    padres[i] = s
                    orden[i] = orden[s] + 1
                    
        
        print("0", self.info(origen))
        i = 1
        while (s != None):
            print(i, self.info(s))
            s = padres[s]
            i += 1
