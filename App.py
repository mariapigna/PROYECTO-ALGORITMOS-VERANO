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


# Creacion del menu
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
                print ()
                for especie in self.lista_especies_obj:
                    especie.show_especie()
                    print ('''_____________________________________________________________________________________________________________________________________________________________________
''')

            elif actividad=='3':
                print ()
                for planeta in self.lista_planetas_obj:
                    planeta.show_planeta()
                    print ('''_____________________________________________________________________________________________________________________________________________________________________
''')
            
            elif actividad=='4':
                print ()
                self.buscar_personaje()
                print ('''_____________________________________________________________________________________________________________________________________________________________________
''')

            elif actividad=='5':
                print ()
                self.grafico_personajes_por_planeta(characters)
                print ('''_____________________________________________________________________________________________________________________________________________________________________
''')

            elif actividad=='6':
                print ()
                self.graficos_caracteristicas_naves(starships)
                print ('''_____________________________________________________________________________________________________________________________________________________________________
''')

            elif actividad=='7':
                print ()
                self.estadisticas_naves(starships)
                print ('''_____________________________________________________________________________________________________________________________________________________________________
''')        

            elif actividad=='8':
                print('''
May the 4th be with you 👽. See you soon ''')
                break

            else:
                print('''
Ingrese una opcion valida! lea bien.
                      ''')
            

    def cargar_API(self, link):
        info=rq.get(link)
        return info.json()
    
# Conversion de pelicula a objeto        
    def cargar_films(self):
        films=self.cargar_API('https://swapi.dev/api/films')
        for pelicula in films['results']:
            self.lista_peliculas_obj.append(Pelicula(pelicula['title'], pelicula['episode_id'], pelicula['opening_crawl'], pelicula['director'], pelicula['release_date']))
            #la siguinete linea me relaciona el link de la pelicula con el titulo de la misma guardado de un diccionario
            self.enlaces_films[pelicula['url']]=pelicula['title']

# Conversion de links de los personajes en la bdd a los nombres de las mismas (linkeo/relacionar)           
    def linkear_personajes(self):
        people=self.cargar_API('https://swapi.dev/api/people')
        # El next es necesario para considerar todas las paginas de API. Se hizo en todos los apartados de esta naturaleza
        url=people['next']
        while url:
            for personaje in people['results']:
                self.enlaces_personajes[personaje['url']]=personaje['name']
            url=people['next']
            if url:
                people=self.cargar_API(url)

    # Conversion de especie a objeto
    def cargar_especies(self):
        species=self.cargar_API('https://swapi.dev/api/species')
        url=species['next']
        while url:
            for especie in species['results']:
                self.enlaces_especies[especie['url']]=especie['name']
                # Creacion de listas para el almacenamiento de las caracteristicas pedidas como nombre mas no como link (para la reduccion de requests)
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

# Conversion de planeta a objeto                
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

# Conversion de personaje a objeto
    def cargar_personajes(self):
        people=self.cargar_API('https://swapi.dev/api/people')
        url=people['next']
        while url:
            for personaje in people['results']:
                lista_films=[]
                lista_naves=[]
                lista_vehiculos=[]
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

# Conversion de links de las naves en la bdd a los nombres de las mismas (linkeo/relacionar)
    def linkear_naves(self):
        starships=self.cargar_API('https://swapi.dev/api/starships')
        url=starships['next']
        while url:
            for nave in starships['results']:
                self.enlaces_naves[nave['url']]=nave['name']
            url=starships['next']
            if url:
                starships=self.cargar_API(url)

# Conversion de links de los vehiculos en la bdd a los nombres de los mismos (linkeo/relacionar)
    def linkear_vehiculos(self):
        vehicles=self.cargar_API('https://swapi.dev/api/vehicles')
        url=vehicles['next']
        while url:
            for vehiculo in vehicles['results']:
                self.enlaces_vehiculos[vehiculo['url']]=vehiculo['name']
            url=vehicles['next']
            if url:
                vehicles=self.cargar_API(url)

# Busqueda de personajes por caracter. Se le anadio el validador por si el usuario no introduce nada o un espacio en blanco.
    def buscar_personaje(self):
        entrada=input('''Ingrese el nombre del personaje de interes: 
- ''')
        if entrada.strip()=='':
            print('''
Debe ingresar al menos un caracter
''')
        else:
            lista_coincidencias=[]
            for personaje in self.lista_personajes_obj:
                if entrada.lower() in personaje.name.lower():
                    lista_coincidencias.append(personaje)
            if lista_coincidencias:        
                for personaje in lista_coincidencias:
                    personaje.show_personaje()
                    print ('''________________________________________________________________________
    ''')
            else:
                print ('''
No hay ninguna coincidencia :(
                    ''')
                
# Funcion validadora en caso de que sea necesario
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

    def graficos_caracteristicas_naves(self, starships_list):
        # a. Longitud de la nave
        starships_df = pd.DataFrame(starships_list)
        # Asegurarse de que la longitud sea numérica
        starships_df['length'] = pd.to_numeric(starships_df['length'], errors='coerce')
        # Ordenar las naves por longitud
        starships_df = starships_df.sort_values(by='length')
        plt.bar(starships_df['name'], starships_df['length'], color='#4790a8')
        # Escala logarítmica
        plt.yscale('log')  
        plt.xticks(rotation=90, fontsize=8)
        plt.xlabel('Naves',fontweight='bold')
        plt.ylabel('Longitud (m)',fontweight='bold')
        plt.title('Longitud de las naves', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.show()

        # b. Capacidad de carga
        # Asegurarse de que la capacidad de carga sea numérica
        starships_df['cargo_capacity'] = pd.to_numeric(starships_df['cargo_capacity'], errors='coerce')
        # Ordenar las naves por capacidad de carga
        starships_df = starships_df.sort_values(by='cargo_capacity')
        plt.bar(starships_df['name'], starships_df['cargo_capacity'], color= '#a85447')
        # Escala logarítmica
        plt.yscale('log')  
        plt.xticks(rotation=90, fontsize=8)
        plt.xlabel('Naves',fontweight='bold')
        plt.ylabel('Capacidad de carga (kg)',fontweight='bold')
        plt.title('Capacidad de carga de las naves', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.show()

        # c. Clasificación de hiperimpulsor
        # Asegurarse de que la hiperimpulsor sea numérica
        starships_df['hyperdrive_rating'] = pd.to_numeric(starships_df['hyperdrive_rating'], errors='coerce')
        # Ordenar las naves por hiperimpulsor
        starships_df = starships_df.sort_values(by='hyperdrive_rating')
        plt.bar(starships_df['name'], starships_df['hyperdrive_rating'], color='#377d52')
        plt.xticks(rotation=90, fontsize=8)
        plt.xlabel('Naves', fontweight='bold')
        plt.ylabel('Clasificación de hiperimpulsor', fontweight='bold')
        plt.title('Clasificación de hiperimpulsor de las naves', fontweight='bold', fontsize=12)
        plt.tight_layout()
        plt.show()

        # d. MGLT (Modern Galactic Light Time)
        # Asegurarse de que la MGLT sea numérica
        starships_df['MGLT'] = pd.to_numeric(starships_df['MGLT'], errors='coerce')
        # Ordenar las naves por MGLT
        starships_df = starships_df.sort_values(by='MGLT')
        plt.bar(starships_df['name'], starships_df['MGLT'], color='#37647d')
        plt.xticks(rotation=90, fontsize=8)
        plt.xlabel('Naves', fontweight='bold')
        plt.ylabel('MGLT', fontweight='bold')
        plt.title('Modern Galactic Light Time de las naves', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.show()   

    def estadisticas_naves(self, starships_list):
        #Convertir la lista a un DataFrame de Pandas
        starships_df = pd.DataFrame(starships_list)
        #Seleccionar columnas específicas, convertir valores a numéricos y calcular estadísticas agregadas
        print(starships_df[
            ["hyperdrive_rating","MGLT","max_atmosphering_speed","cost_in_credits"]
        ].apply(pd.to_numeric, errors = "coerce").aggregate(["mean",statistics.mode,"max","min"]))    