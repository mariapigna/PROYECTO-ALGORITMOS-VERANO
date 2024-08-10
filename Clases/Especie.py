class Especie:
    def __init__(self, name, average_height, classification, homeworld, language, people, films):
        self.name=name
        self.average_height=average_height
        self.classification=classification
        self.homeworld=homeworld
        self.language=language
        self.people=people
        self.films=films
        self.arreglar_lista()

    def show_especie(self):
        print (f'''ESPECIE: {self.name}
Altura: {self.average_height}
Clasificacion: {self.classification}
Planeta de origen: {self.homeworld}
Lengua materna: {self.language}
Personajes de la especie: {self.people}
Peliculas donde aparece esta especie: {self.films}''')
        
    def arreglar_lista(self):
        self.people= ', '.join(self.people)
        self.films=', '.join(self.films)