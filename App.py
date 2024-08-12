import requests as rq
import matplotlib.pyplot as plt
import pandas as pd
import csv
import statistics
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
        characters, planets, starships, weapons = self.cargar_datos()


        while True:
            print(f'''*/*/*/*/*/* BIENVENIDO GEEK */*/*/*/*
    Elija la opcion que desea consultar (numero):
1. Ver peliculas de la SAGA 🎞️
2. Ver lista de especies de seres vivos 🧎
3. Ver lista de planetas 🪐
4. Buscar personaje 👀
5. Grafico de cantidad de personajes nacidos en cada planeta
6. Graficos de caracteristicas de naves
7. Estadisticas sobre las naves
8. Salir 💨
''')
            actividad=input('-------> ')
            if actividad=='1':
                print()
                for pelicula in self.lista_peliculas_obj:
                    pelicula.show_pelicula()
                    print ('''_____________________________________________________________________________________________________________________________________________________________________
''')

            elif actividad=='2':
                for especie in self.lista_especies_obj:
                    especie.show_especie()
                    print ('''_____________________________________________________________________________________________________________________________________________________________________
''')

            elif actividad=='3':
                for planeta in self.lista_planetas_obj:
                    planeta.show_planeta()
                    print ('''_____________________________________________________________________________________________________________________________________________________________________
''')
            
            elif actividad=='4':
                self.buscar_personaje()
                print ('''_____________________________________________________________________________________________________________________________________________________________________
''')

            elif actividad=='5':
                self.grafico_personajes_por_planeta(characters)
                print ('''_____________________________________________________________________________________________________________________________________________________________________
''')

            elif actividad=='6':
                print("Opcion 6")

            elif actividad=='7':
                print("Opcion 7")        

            elif actividad=='8':
                print('May the 4th be with you 👽')
                break

            else:
                print('Ingrese una opcion valida! lea bien.')
            








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
                self.lista_planetas_obj.append(Planeta(planeta['name'], planeta['rotation_period'], planeta['orbital_period'], planeta['climate'], planeta['population'], lista_people, lista_films))
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
                lista_planetas=[]
                lista_especies=[]
                for pelicula in personaje['films']:
                    lista_films.append(self.enlaces_films[pelicula])
                for nave in personaje['starships']:
                    lista_naves.append(self.enlaces_naves[nave])
                for vehiculo in personaje['vehicles']:
                    lista_vehiculos.append(self.enlaces_vehiculos[vehiculo])
                for especie in personaje['species']:
                    lista_especies.append(self.enlaces_especies[especie])
                self.lista_personajes_obj.append(Personaje(personaje['name'], personaje['gender'], self.enlaces_planetas[personaje['homeworld']], lista_films, lista_especies, lista_naves, lista_vehiculos))
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

    def buscar_personaje(self):
        entrada=input('''Ingrese el nombre del personaje de interes: 
- ''')
        lista_coincidencias=[]
        for personaje in self.lista_personajes_obj:
            if entrada.lower() in personaje.name.lower():
                lista_coincidencias.append(personaje)
        for personaje in lista_coincidencias:
            personaje.show_personaje()
    
    def validar(dato, validacion, lista=[]):
            None

    def cargar_datos(self):
        characters = []
        planets = []
        starships = []
        weapons = []
    
        with open('./characters.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                characters.append(row)

        with open('./planets.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                planets.append(row)

        with open('./starships.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                starships.append(row)

        with open('./weapons.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                weapons.append(row)
    
        return characters, planets, starships, weapons

    

    def grafico_personajes_por_planeta(self, characters_list):
        
        #Se crea la data de los personajes
        characters_df = pd.DataFrame(characters_list)
        planet_counts = characters_df['homeworld'].value_counts()
        #Se crea la grafica
        plt.bar(planet_counts.index, planet_counts.values, color='#564bad')
        plt.xticks(rotation=90, fontsize=8)
        plt.xlabel('Planeta', fontweight='bold')
        plt.ylabel('Cantidad de personajes', fontweight='bold')
        plt.legend(["Cantidades por planeta"])
        plt.title('Personajes nacidos en cada planeta', fontsize=12, fontweight='bold')
        #para que la grafica se ajuste bien en la pestaña emergente
        plt.tight_layout()
        plt.show()