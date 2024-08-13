class Integrante:
    def __init__(self, id, nombre, especie, genero):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
    
    def __str__(self):
        return f"{self.nombre} ({self.especie} - {self.genero})"
