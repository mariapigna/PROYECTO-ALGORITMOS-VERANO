class Personaje:
    def __init__(self, name, gender, homeworld, films, species, starships, vehicles):
        self.name=name
        self.gender=gender
        self.homeworld=homeworld
        self.films=films
        self.species=species
        self.starships=starships
        self.vehicles=vehicles
        self.arreglar_lista_vacia()

    def arreglar_lista_vacia(self):
        if not self.films:
            self.films='No definido'
        else:
            self.films=', '.join(self.films)
        if not self.species:
            self.species='No categorizado'
        else:
            self.species=', '.join(self.species)
        if not self.starships:
            self.starships='No posee nave'
        else:
            self.starships=', '.join(self.starships)
        if not self.vehicles:
            self.vehicles='No posee vehiculo'
        else:
            self.vehicles=', '.join(self.vehicles)

    def show_personaje(self):
        print(f'''NOMBRE: {self.name}
Planeta de origen: {self.homeworld}
Titulos en los que aparece: {self.films}
Genero: {self.gender}
Especie: {self.species}
Naves utilizados: {self.starships}
Vehiculos utilizados: {self.vehicles}''')