class Arma:
    def __init__(self, id, nombre, modelo, fabricante, tipo, descripcion):
        self.id = id
        self.nombre = nombre
        self.modelo = modelo
        self.fabricante = fabricante
        self.tipo = tipo
        self.descripcion = descripcion
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo}): {self.descripcion}"
