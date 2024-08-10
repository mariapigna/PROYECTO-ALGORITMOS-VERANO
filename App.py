import requests as rq
from Clases.Pelicula import Pelicula
from Clases.Especie import Especie
from Clases.Planeta import Planeta
from Clases.Personaje import Personaje
class App:
    lista_peliculas_obj=[]
    lista_especies_obj=[]
    lista_planetas_obj=[]
    lista_personajes_obj=[]
    enlaces_films={}
    enlaces_personajes={}
    enlaces_especies={}
    enlaces_planetas={}
    enlaces_naves={}
    enlaces_vehiculos={}
    def start(self):
        self.cargar_films()
        self.linkear_personajes()
        self.cargar_planetas()
        self.cargar_especies()
        self.linkear_naves()
        self.linkear_vehiculos()
        self.cargar_personajes()
        print (self.lista_especies_obj)
        print (self.lista_peliculas_obj)
        print(self.lista_personajes_obj)
        print(self.lista_planetas_obj)

    def cargar_API(self, link):
        info=rq.get(link)
        return info.json()
        
    def cargar_films(self):
        films=self.cargar_API('https://swapi.dev/api/films')
        for pelicula in films['results']:
            self.lista_peliculas_obj.append(Pelicula(pelicula['title'], pelicula['episode_id'], pelicula['opening_crawl'], pelicula['director'], pelicula['release_date']))
            #la siguinete linea me relaciona el link de la pelicula con el titulo de la misma guardado de un diccionario
            self.enlaces_films[pelicula['url']]=pelicula['title']
            
    def linkear_personajes(self):
        people=self.cargar_API('https://swapi.dev/api/people')
        url=people['next']
        while url:
            for personaje in people['results']:
                self.enlaces_personajes[personaje['url']]=personaje['name']
            url=people['next']
            if url:
                people=self.cargar_API(url)

    def cargar_especies(self):
        species=self.cargar_API('https://swapi.dev/api/species')
        url=species['next']
        while url:
            for especie in species['results']:
                self.enlaces_especies[especie['url']]=especie['name']
                lista_people=[]
                lista_films=[]
                for personaje in especie['people']:
                    lista_people.append(self.enlaces_personajes[personaje])
                for pelicula in especie['films']:
                    lista_films.append(self.enlaces_films[pelicula])
                if especie['homeworld']:
                    self.lista_especies_obj.append(Especie(especie['name'], especie['average_height'], especie['classification'], self.enlaces_planetas[especie['homeworld']], especie['language'], lista_people, lista_films))
                else:
                    self.lista_especies_obj.append(Especie(especie['name'], especie['average_height'], especie['classification'], None, especie['language'], lista_people, lista_films))
            url=species['next']
            if url:
                species=self.cargar_API(url)
                
    def cargar_planetas(self):
        planets=self.cargar_API('https://swapi.dev/api/planets')
        url=planets['next']
        while url:
            for planeta in planets['results']:
                self.enlaces_planetas[planeta['url']]=planeta['name']
                lista_people=[]
                lista_films=[]
                for personaje in planeta['residents']:
                    lista_people.append(self.enlaces_personajes[personaje])
                for pelicula in planeta['films']:
                    lista_films.append(self.enlaces_films[pelicula])
                self.lista_especies_obj.append(Planeta(planeta['name'], planeta['rotation_period'], planeta['orbital_period'], planeta['climate'], planeta['population'], planeta['residents'], planeta['films']))
            url=planets['next']
            if url:
                planets=self.cargar_API(url)

    def cargar_personajes(self):
        people=self.cargar_API('https://swapi.dev/api/people')
        url=people['next']
        while url:
            for personaje in people['results']:
                lista_films=[]
                lista_naves=[]
                lista_vehiculos=[]
                for pelicula in personaje['films']:
                    lista_films.append(self.enlaces_films[pelicula])
                for nave in personaje['starships']:
                    lista_naves.append(self.enlaces_naves[nave])
                for vehiculo in personaje['vehicles']:
                    lista_vehiculos.append(self.enlaces_vehiculos[vehiculo])
                self.lista_personajes_obj.append(Personaje(personaje['name'], personaje['gender'], personaje['homeworld'], lista_films, personaje['species'], lista_naves, lista_vehiculos))
            url=people['next']
            if url:
                people=self.cargar_API(url)

    def linkear_naves(self):
        starships=self.cargar_API('https://swapi.dev/api/starships')
        url=starships['next']
        while url:
            for nave in starships['results']:
                self.enlaces_naves[nave['url']]=nave['name']
            url=starships['next']
            if url:
                starships=self.cargar_API(url)

    def linkear_vehiculos(self):
        vehicles=self.cargar_API('https://swapi.dev/api/vehicles')
        url=vehicles['next']
        while url:
            for vehiculo in vehicles['results']:
                self.enlaces_vehiculos[vehiculo['url']]=vehiculo['name']
            url=vehicles['next']
            if url:
                vehicles=self.cargar_API(url)

