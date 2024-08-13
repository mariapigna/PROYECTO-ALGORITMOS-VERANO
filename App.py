import requests as rq
import matplotlib.pyplot as plt
import pandas as pd
import csv
from Clases.Mision import Mision
from Clases.PlanetaCSV import PlanetaCSV
from Clases.Nave import Nave
from Clases.Arma import Arma
from Clases.Integrante import Integrante
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
5. Grafico de cantidad de personajes nacidos en cada planeta 📈
6. Graficos de caracteristicas de naves 📈
7. Estadisticas sobre las naves 📎
8. Configurar misiones ⚙️
9. Salir 💨
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
                self.buscar_personaje()

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
                self.menu_misiones(characters, planets, starships, weapons)
                print ('''_____________________________________________________________________________________________________________________________________________________________________
''')        
            elif actividad=='9':
                print('''
May the 4th be with you 👽. See you soon
''')
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

    def cargar_datos(self):
        characters = []
        planets = []
        starships = []
        weapons = []
        with open('./starwars/csv/characters.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                characters.append(row)
        with open('./starwars/csv/planets.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                planets.append(row)
        with open('./starwars/csv/starships.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                starships.append(row)
        with open('./starwars/csv/weapons.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                weapons.append(row)
        return characters, planets, starships, weapons

    def mostrar_menu(self):
        print("1. Crear nueva misión 💬")
        print("2. Modificar misión existente ✏️")
        print("3. Ver misiones 👀")
        print("4. Guardar misiones 💾")
        print("5. Cargar misiones ☁️")
        print("6. Eliminar misión ❌")
        print("7. Salir 💨\n")

    def crear_mision(self, planets, starships, weapons, characters, misiones):
        nombre_valido = False
        while not nombre_valido:
            nombre = input("Nombre de la misión: ").strip()
            # Validar si el nombre de la misión ya existe
            if any(mision.nombre.lower() == nombre.lower() for mision in misiones):
                print("Ya existe una misión con ese nombre. Por favor, elige un nombre diferente.")
                continue

            if not nombre:
                print("El nombre de la misión no puede estar vacío.")
                continue
            nombre_valido = True  # Si el nombre es único y no está vacío, es válido

        # Validar la selección del planeta
        planeta_seleccionado = None
        while planeta_seleccionado is None:
            print("\nSelecciona un planeta (numero):")
            for idx, row in enumerate(planets):
                print(f"{idx + 1}. {row['name']}")
            print()
            seleccion = input("-------> ").strip()

            if not seleccion.isdigit():
                print("Entrada no válida. Debes ingresar un número.")
                continue
            seleccion = int(seleccion) - 1

            if 0 <= seleccion < len(planets):
                planeta_fila = planets[seleccion]
                planeta = PlanetaCSV(planeta_fila['id'], planeta_fila['name'], planeta_fila['climate'], planeta_fila['terrain'])
                planeta_seleccionado = planeta
            else:
                print("Selección no válida. Por favor, selecciona un número válido.")

        # Seleccionar nave
        nave_seleccionada = None
        while nave_seleccionada is None:
            print("\nSelecciona una nave:")
            for idx, row in enumerate(starships):
                print(f"{idx + 1}. {row['name']}")
            print()
            seleccion = input("-------> ").strip()
            if not seleccion.isdigit():
                print("Entrada no válida. Debes ingresar un número.")
                continue
            seleccion = int(seleccion) - 1

            if 0 <= seleccion < len(starships):
                nave_fila = starships[seleccion]
                nave = Nave(nave_fila['id'], nave_fila['name'], nave_fila['model'], nave_fila['manufacturer'], nave_fila['starship_class'], nave_fila['crew'])
                nave_seleccionada = nave
            else:
                print("Selección no válida. Por favor, selecciona un número válido.")

        # Seleccionar armas (permitiendo duplicados)
        armas = []
        print("Selecciona armas (hasta 7) (numero):")
        print ('--Ingrese 0 para terminar la seleccion--')
        print()
        while len(armas) < 7:
            for idx, row in enumerate(weapons):
                print(f"{idx + 1}. {row['name']}")
            print()
            seleccion = input("-------> ").strip()
            
            if seleccion == '0':
                break
            
            if not seleccion.isdigit():
                print("Entrada no válida. Debes ingresar un número.")
                continue
            seleccion = int(seleccion) - 1

            if 0 <= seleccion < len(weapons):
                arma_fila = weapons[seleccion]
                arma = Arma(arma_fila['id'], arma_fila['name'], arma_fila['model'], arma_fila['manufacturer'], arma_fila['type'], arma_fila['description'])
                armas.append(arma)
                print(f"Arma {arma.nombre} agregada.\n")
            else:
                print("Selección no válida. Por favor, selecciona un número válido.")

        # Seleccionar integrantes (sin duplicados)
        integrantes = []
        print()
        print("Selecciona integrantes (hasta 7) (numero)::")
        print ('--Ingrese 0 para terminar la seleccion--\n')
        while len(integrantes) < 7:
            for idx, row in enumerate(characters):
                print(f"{idx + 1}. {row['name']}")
            print()
            seleccion = input("-------> ").strip()
            
            if seleccion == '0':
                break
            
            if not seleccion.isdigit():
                print("Entrada no válida. Debes ingresar un número.\n")
                continue
            seleccion = int(seleccion) - 1

            if 0 <= seleccion < len(characters):
                integrante_fila = characters[seleccion]
                # Verificar si el integrante ya ha sido agregado
                if not any(integrante.nombre == integrante_fila['name'] for integrante in integrantes):
                    integrante = Integrante(integrante_fila['id'], integrante_fila['name'], integrante_fila['species'], integrante_fila['gender'])
                    integrantes.append(integrante)
                    print(f"Integrante {integrante.nombre} agregado.\n")
                else:
                    print("Este integrante ya ha sido seleccionado. Por favor, elige otro.\n")
            else:
                print("Selección no válida. Por favor, selecciona un número válido.\n")

        # Crear la misión
        mision = Mision(nombre, planeta_seleccionado, nave_seleccionada, armas, integrantes)
        print("\n***** Misión creada con éxito! *****")
        print(mision)
        return mision


    def modificar_mision(self, mision, planets, starships, weapons, characters):
        while True:
            print(f"\nModificando misión: {mision.nombre}")
            print("1. Modificar nombre")
            print("2. Modificar planeta")
            print("3. Modificar nave")
            print("4. Modificar armas")
            print("5. Modificar integrantes")
            print("6. Regresar al menú principal de modificación\n")

            opcion = input("-------> ")

            if opcion == "1":
                nuevo_nombre = input("\nNuevo nombre de la misión: ").strip()
                mision.nombre = nuevo_nombre
                print(f"Nombre cambiado a {nuevo_nombre}")

            elif opcion == "2":
                print('''
Selecciona un nuevo planeta (numero):''')
                for idx, row in enumerate(planets):
                    print(f"{idx + 1}. {row['name']}")
                print()
                seleccion = input("-------> ").strip()
                if seleccion.isdigit() and 0 <= int(seleccion) - 1 < len(planets):
                    planeta_fila = planets[int(seleccion) - 1]
                    nuevo_planeta = PlanetaCSV(planeta_fila['id'], planeta_fila['name'], planeta_fila['climate'], planeta_fila['terrain'])
                    mision.planeta = nuevo_planeta
                    print(f"Planeta cambiado a {nuevo_planeta.nombre}")
                else:
                    print("Selección no válida.")

            elif opcion == "3":
                print("\nSelecciona una nueva nave (numero):")
                for idx, row in enumerate(starships):
                    print(f"{idx + 1}. {row['name']}")
                print()
                seleccion = input("-------> ").strip()
                if seleccion.isdigit() and 0 <= int(seleccion) - 1 < len(starships):
                    nave_fila = starships[int(seleccion) - 1]
                    nueva_nave = Nave(nave_fila['id'], nave_fila['name'], nave_fila['model'], nave_fila['manufacturer'], nave_fila['starship_class'], nave_fila['crew'])
                    mision.nave = nueva_nave
                    print(f"Nave cambiada a {nueva_nave.nombre}")
                else:
                    print("Selección no válida.")

            elif opcion == "4":  # Modificar armas
                while True:
                    print("\nModificar armas (numero):")
                    print(f"+++++ Armas actuales ({len(mision.armas)}/7):")
                    for idx, arma in enumerate(mision.armas):
                        print(f"{idx + 1}. {arma.nombre}")
                    print()
                    print('Accion a realizar: ')
                    print("1. Agregar arma")
                    print("2. Eliminar arma")
                    print("3. Regresar")
                    print()
                    opcion_arma = input("-------> ")

                    if opcion_arma == "1":
                        if len(mision.armas) < 7:
                            for idx, row in enumerate(weapons):
                                print(f"{idx + 1}. {row['name']}")
                            print()
                            seleccion = input("-------> ").strip()
                            if seleccion.isdigit() and 0 <= int(seleccion) - 1 < len(weapons):
                                arma_fila = weapons[int(seleccion) - 1]
                                nueva_arma = Arma(arma_fila['id'], arma_fila['name'], arma_fila['model'], arma_fila['manufacturer'], arma_fila['type'], arma_fila['description'])
                                mision.armas.append(nueva_arma)
                                print(f"Arma agregada: {nueva_arma.nombre}")
                            else:
                                print("Selección no válida.")
                        else:
                            print("No puedes agregar más armas. El máximo es 7.")

                    elif opcion_arma == "2":
                        for idx, arma in enumerate(mision.armas):
                            print(f"{idx + 1}. {arma.nombre}")
                        print()
                        seleccion = input("-------> ").strip()
                        if seleccion.isdigit() and 0 <= int(seleccion) - 1 < len(mision.armas):
                            arma_a_eliminar = mision.armas[int(seleccion) - 1]
                            mision.armas.remove(arma_a_eliminar)
                            print(f"Arma eliminada: {arma_a_eliminar.nombre}")
                        else:
                            print("Selección no válida.")

                    elif opcion_arma == "3":
                        break
                    else:
                        print("Opción no válida.")

            elif opcion == "5":  # Modificar integrantes
                while True:
                    print("\nModificar integrantes (numero):")
                    print(f"+++++ Integrantes actuales ({len(mision.integrantes)}/7):")
                    for idx, integrante in enumerate(mision.integrantes):
                        print(f"{idx + 1}. {integrante.nombre}")
                    print()
                    print('Accion a realizar: ')
                    print("1. Agregar integrante")
                    print("2. Eliminar integrante")
                    print("3. Regresar")
                    print()
                    opcion_integrante = input("-------> ")
                    if opcion_integrante == "1":
                        if len(mision.integrantes) < 7:
                            for idx, row in enumerate(characters):
                                print(f"{idx + 1}. {row['name']}")
                            print()
                            seleccion = input("-------> ").strip()
                            if seleccion.isdigit() and 0 <= int(seleccion) - 1 < len(characters):
                                integrante_fila = characters[int(seleccion) - 1]
                                if not any(integrante.nombre == integrante_fila['name'] for integrante in mision.integrantes):
                                    nuevo_integrante = Integrante(integrante_fila['id'], integrante_fila['name'], integrante_fila['species'], integrante_fila['gender'])
                                    mision.integrantes.append(nuevo_integrante)
                                    print(f"Integrante agregado: {nuevo_integrante.nombre}\n")
                                else:
                                    print("Este integrante ya ha sido seleccionado. Por favor, elige otro.")
                            else:
                                print("Selección no válida.")
                        else:
                            print("No puedes agregar más integrantes. El máximo es 7.")
                    elif opcion_integrante == "2":
                        for idx, integrante in enumerate(mision.integrantes):
                            print(f"{idx + 1}. {integrante.nombre}")
                        seleccion = input("Número del integrante a eliminar: ").strip()
                        if seleccion.isdigit() and 0 <= int(seleccion) - 1 < len(mision.integrantes):
                            integrante_a_eliminar = mision.integrantes[int(seleccion) - 1]
                            mision.integrantes.remove(integrante_a_eliminar)
                            print(f"Integrante eliminado: {integrante_a_eliminar.nombre}")
                        else:
                            print("Selección no válida.")
                    elif opcion_integrante == "3":
                        break
                    else:
                        print("Opción no válida.")

            elif opcion == "6":
                break  # Regresar al menú principal
            else:
                print("Opción no válida.")

    def modificar_mision_detalle(self, misiones, planets, starships, weapons, characters):
        if not misiones:
            print("No hay misiones disponibles para modificar.")
            return

        while True:
            print("Selecciona una misión para modificar (numero):")
            for idx, m in enumerate(misiones):
                print(f"{idx + 1}. {m.nombre}")
            print()
            seleccion = input("-------> ").strip()

            if not seleccion.isdigit():
                print("Entrada no válida. Debes ingresar un número.")
                continue
            
            seleccion = int(seleccion) - 1

            if 0 <= seleccion < len(misiones):
                mision = misiones[seleccion]
                self.modificar_mision(mision, planets, starships, weapons, characters)
                break
            else:
                print("Selección no válida. Por favor, selecciona un número dentro del rango.")

    def eliminar_mision(self, misiones):
        if not misiones:
            print("No hay misiones disponibles para eliminar.")
            return

        while True:
            print("Selecciona una misión para eliminar:")
            for idx, m in enumerate(misiones):
                print(f"{idx + 1}. {m.nombre}")
            print()
            seleccion = input("-------> ").strip()

            if not seleccion.isdigit():
                print("Entrada no válida. Debes ingresar un número.")
                continue
            
            seleccion = int(seleccion) - 1

            if 0 <= seleccion < len(misiones):
                mision_eliminada = misiones.pop(seleccion)
                print(f"La misión '{mision_eliminada.nombre}' ha sido eliminada.")
                break
            else:
                print("Selección no válida. Por favor, selecciona un número dentro del rango.")

    def ver_mision_detalle(self, misiones):
        if not misiones:
            print("No hay misiones disponibles para ver.")
            return

        while True:
            print("Selecciona una misión para ver los detalles:")
            for idx, m in enumerate(misiones):
                print(f"{idx + 1}. {m.nombre}")
            print()
            seleccion = input("-------> ").strip()

            if not seleccion.isdigit():
                print("Entrada no válida. Debes ingresar un número.")
                continue
            
            seleccion = int(seleccion) - 1

            if 0 <= seleccion < len(misiones):
                mision = misiones[seleccion]
                print("\nDetalles de la misión:")
                print(mision)
                break
            else:
                print("Selección no válida. Por favor, selecciona un número dentro del rango.")

    def menu_misiones(self, characters, planets, starships, weapons):

        misiones = []
        while True:
            print('''
Elija la opcion que desea consultar (numero): ''')
            self.mostrar_menu()
            opcion = input("-------> ")
            print()
            if opcion == "1":
                if len(misiones) >= 5:
                    print("No puedes crear más de 5 misiones.")
                else:
                    mision = self.crear_mision(planets, starships, weapons, characters, misiones)
                    if mision:
                        misiones.append(mision)
            elif opcion == "2":
                self.modificar_mision_detalle(misiones, planets, starships, weapons, characters)
            elif opcion == "3":  # Ver misiones
                self.ver_mision_detalle(misiones)
            elif opcion == "4":
                nombre_archivo = input("Nombre del archivo para guardar las misiones: ")
                if nombre_archivo.count('.')==0 and nombre_archivo.count(' ')==0:
                    Mision.guardar_misiones(misiones,nombre_archivo)
                    print(f"Misiones guardadas en {nombre_archivo}")
                else:
                    print('No son validos ni puntos ni espacios')
            elif opcion == "5":
                nombre_archivo = input("Nombre del archivo para cargar las misiones: ")
                if nombre_archivo.count('.')==0 and nombre_archivo.count(' ')==0:
                    misiones_cargadas = Mision.cargar_de_archivo(nombre_archivo,weapons,planets,characters,starships)  # Cargar las misiones desde el archivo
                    if misiones_cargadas:
                        misiones=misiones_cargadas  # Agregar las misiones cargadas a la lista existente
                        print("Misiones cargadas con éxito.")
                    else:
                        print("No se pudieron cargar misiones.")
                else: 
                    print('No son validos ni puntos ni espacios')
            elif opcion == "6":
                self.eliminar_mision(misiones)
            elif opcion == "7":
                print("Saliendo...")
                break
            else:
                print("Opción no válida, por favor intenta de nuevo.")



        