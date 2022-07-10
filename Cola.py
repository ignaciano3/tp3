class Cola:

    def __init__(self):
        self.cola = []

    def esta_vacia(self):
        return len(self.cola) == 0
        
    def encolar(self, item):
        if (item in self.cola): print("repetciones")
        self.cola.append(item)

    def ver_primero(self):
        return self.cola[0]

    def desencolar(self):
        if len(self.cola) < 1:
            return None
        return self.cola.pop(0)