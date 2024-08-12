from PlanetaCSV import PlanetaCSV  
from Nave import Nave

class Mision:
    def __init__(self, nombre, planeta, nave, armas, integrantes):
        self.nombre = nombre
        self.planeta = planeta
        self.nave = nave
        self.armas = armas
        self.integrantes = integrantes
    
    def modificar_nombre(self, nuevo_nombre):
        self.nombre = nuevo_nombre

    def modificar_planeta(self, nuevo_planeta):
        self.planeta = nuevo_planeta
    
    def modificar_nave(self, nueva_nave):
        self.nave = nueva_nave
    
    def agregar_arma(self, arma):
        if len(self.armas) < 7:
            self.armas.append(arma)
        else:
            print("No puedes agregar más de 7 armas.")
    
    def eliminar_arma(self, arma):
        if arma in self.armas:
            self.armas.remove(arma)
    
    def agregar_integrante(self, integrante):
        if len(self.integrantes) < 7:
            self.integrantes.append(integrante)
        else:
            print("No puedes agregar más de 7 integrantes.")
    
    def eliminar_integrante(self, integrante):
        if integrante in self.integrantes:
            self.integrantes.remove(integrante)
    
    def __str__(self):
        armas_str = "\n".join([str(arma) for arma in self.armas]) if self.armas else "No hay armas seleccionadas"
        integrantes_str = "\n".join([str(integrante) for integrante in self.integrantes]) if self.integrantes else "No hay integrantes seleccionados"
        
        return (f"Misión: {self.nombre}\n"
                f"Planeta: {self.planeta}\n"
                f"Nave: {self.nave}\n"
                f"Armas:\n{armas_str}\n"
                f"Integrantes:\n{integrantes_str}\n")

    def cargar_de_archivo(nombre_archivo):
        misiones = []
        try:
            with open(nombre_archivo, 'r') as file:
                contenido = file.read().strip()
                misiones_texto = contenido.split("\n\n")  # Cada misión está separada por un doble salto de línea
                
                for mision_texto in misiones_texto:
                    lineas = mision_texto.split("\n")
                    nombre = lineas[0].replace("Misión: ", "").strip()
                    
                    # Verificación de formato correcto para la línea del planeta
                    planeta_info = lineas[1].replace("Planeta: ", "").strip().split(", ")
                    if len(planeta_info) != 3:
                        print(f"Error al leer el planeta para la misión '{nombre}'. Formato inesperado: {planeta_info}")
                        continue
                    
                    planeta = PlanetaCSV(1, planeta_info[0], planeta_info[1], planeta_info[2])
                    
                    # Extraer la nave (esto es un ejemplo y puede necesitar ajustes)
                    nave_info = lineas[2].replace("Nave: ", "").split(":")
                    nave = Nave(1, nave_info[0], nave_info[1].split(" ")[1], "Desconocido", "Desconocido", 1)
                    
                    armas = []  # Agregar lógica para extraer armas si es necesario
                    integrantes = []  # Similar para los integrantes
                    
                    misiones.append(Mision(nombre, planeta, nave, armas, integrantes))
                    
        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no existe.")
        
        return misiones