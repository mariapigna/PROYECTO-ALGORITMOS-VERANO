from Clases.PlanetaCSV import PlanetaCSV  
from Clases.Nave import Nave
from Clases.Integrante import Integrante
from Clases.Arma import Arma
import json

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
        armas_str = "\n > ".join([str(arma) for arma in self.armas]) if self.armas else "No hay armas seleccionadas"
        integrantes_str = "\n > ".join([str(integrante) for integrante in self.integrantes]) if self.integrantes else "No hay integrantes seleccionados"
        
        return (f"\n*/ {self.nombre} /*\n\n"
                f'''Planeta: \n > {self.planeta}\n'''
                f'''Nave: \n > {self.nave}\n'''
                f"Armas: \n > {armas_str}\n"
                f"Integrantes:\n > {integrantes_str}\n")

    def cargar_de_archivo(nombre_archivo,armas,planetas,personajes,naves):
        try:
            misiones=[]
            with open(f'{nombre_archivo}.json','r') as f:
                datos=json.load(f)
                for mision in datos:
                    planeta_fila = planetas[mision['planeta']-1]
                    planeta = PlanetaCSV(planeta_fila['id'], planeta_fila['name'], planeta_fila['climate'], planeta_fila['terrain'])
                    nave_fila = naves[mision['nave']-1]
                    nave = Nave(nave_fila['id'], nave_fila['name'], nave_fila['model'], nave_fila['manufacturer'], nave_fila['starship_class'], nave_fila['crew'])
                    integrantes= []
                    for integrante in mision['integrantes']:
                        integrante_fila = personajes[integrante-1]
                        integrantes.append(Integrante(integrante_fila['id'], integrante_fila['name'], integrante_fila['species'], integrante_fila['gender']))
                    armas_selec=[]
                    for arma in mision['armas']:
                        arma_fila = armas[arma-1]
                        armas_selec.append(Arma(arma_fila['id'], arma_fila['name'], arma_fila['model'], arma_fila['manufacturer'], arma_fila['type'], arma_fila['description']))
                    misiones.append(Mision(mision['name'],planeta, nave, armas_selec,integrantes))

        
            return misiones
        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no existe.")
        
        
    
    def mision_guardado(self):
        dic={
            'name':self.nombre,
            'planeta':int(self.planeta.id),
            'nave':int(self.nave.id),
            'armas':[int(x.id) for x in self.armas],
            'integrantes': [int(x.id) for x in self.integrantes]
        }
        return dic
    
    def guardar_misiones(misiones, nombre):
        misiones_guardar=[]
        for mision in misiones:
            misiones_guardar.append(mision.mision_guardado())
        with open(f'{nombre}.json','w') as f:
            f.write(json.dumps(misiones_guardar))
    