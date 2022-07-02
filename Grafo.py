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