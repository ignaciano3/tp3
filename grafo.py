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
    
    # Devuelve informacion de la arista
    def peso(self, src, dest):
        return self.graph[src][dest]
    
    # Devuelve informacion del vertice
    def info(self, v):
        return self.data[v]

    def adyacentes(self, v):
        ady = list()
        for i in self.graph[v].keys():
            ady.append(i)
        return ady