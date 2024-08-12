class PlanetaCSV:
    def __init__(self, id, nombre, clima, terreno):
        self.id = id
        self.nombre = nombre
        self.clima = clima
        self.terreno = terreno
    
    def __str__(self):
        return f"{self.nombre}: Clima {self.clima}, Terreno {self.terreno}"
