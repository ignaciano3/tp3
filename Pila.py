class Pila:
    def __init__(self):
        self.pila = []

    def esta_vacia(self):
        return len(self.pila) == 0
        
    def apilar(self, item):
        self.pila.insert(0, item)

    def ver_primero(self):
        return self.pila[0]

    def desapilar(self):
        if len(self.pila) < 1:
            return None
        return self.pila.pop(0)