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

class UnionFind:
    def __init__(self, largo):
        self.uf = [i for i in range(largo)]
        self.rank = [0 for _ in range(largo)]
    
    def find(self, v):
        if self.uf[v] == v:
            return v
        else:
            return self.find(self.uf[v])
    
    def union(self, v1, v2):
        v1root = self.find(v1)
        v2root = self.find(v2)

        if self.rank[v1root] < self.rank[v2root]:
            self.uf[v1root] = v2root
        elif self.rank[v1root] > self.rank[v2root]:
            self.uf[v2root] = v1root
        else:
            self.uf[v2root] = v1root
            self.rank[v1root] +=1
    
    def print_uf(self):
        print([chr(i+65) for i in self.uf])