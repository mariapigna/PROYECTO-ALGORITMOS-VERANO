class Planeta:
    def __init__(self, name, rotation_period, orbital_period, climate, population, residents, films):
        self.name=name
        self.rotation_period=rotation_period
        self.orbital_period=orbital_period
        self.climate=climate
        self.population=population
        self.residents=residents
        self.films=films
        self.arreglar_lista_vacia()

    def arreglar_lista_vacia(self):
        if not self.films:
            self.films='Ninguno'
        else:
            self.films=', '.join(self.films)
        if not self.residents:
            self.residents='Ninguno'
        else:
            self.residents=', '.join(self.residents)

    def show_planeta(self):
        print(f'''NOMBRE: {self.name}
Periodo de orbita: {self.orbital_period}
Periodo de rotacion:{self.rotation_period}
Cantidad de habitantes: {self.population}
Tipo de clima: {self.climate}
Episodios en los que aparece: {self.films}
Personajes originarios del planeta: {self.residents}''')