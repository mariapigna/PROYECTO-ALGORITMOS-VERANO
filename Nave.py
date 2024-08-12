class Nave:
    def __init__(self, id, nombre, modelo, fabricante, clase, tripulacion):
        self.id = id
        self.nombre = nombre
        self.modelo = modelo
        self.fabricante = fabricante
        self.clase = clase
        self.tripulacion = tripulacion
    
    def __str__(self):
        return f"{self.nombre} ({self.clase}): Modelo {self.modelo} por {self.fabricante}"
