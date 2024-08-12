import csv
from Mision import Mision
from PlanetaCSV import PlanetaCSV
from Nave import Nave
from Arma import Arma
from Integrante import Integrante

def cargar_datos():
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

def mostrar_menu():
    print("1. Crear nueva misión")
    print("2. Modificar misión existente")
    print("3. Ver misiones")
    print("4. Guardar misiones")
    print("5. Cargar misiones")
    print("6. Eliminar misión")
    print("7. Salir")

def crear_mision(planets, starships, weapons, characters, misiones):
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
        print("Selecciona un planeta:")
        for idx, row in enumerate(planets):
            print(f"{idx + 1}. {row['name']}")
        
        seleccion = input("Número del planeta: ").strip()
        
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
        print("Selecciona una nave:")
        for idx, row in enumerate(starships):
            print(f"{idx + 1}. {row['name']}")
        
        seleccion = input("Número de la nave: ").strip()
        
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
    print("Selecciona armas (hasta 7):")
    while len(armas) < 7:
        for idx, row in enumerate(weapons):
            print(f"{idx + 1}. {row['name']}")
        
        seleccion = input("Número del arma (0 para terminar): ").strip()
        
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
            print(f"Arma {arma.nombre} agregada.")
        else:
            print("Selección no válida. Por favor, selecciona un número válido.")

    # Seleccionar integrantes (sin duplicados)
    integrantes = []
    print("Selecciona integrantes (hasta 7):")
    while len(integrantes) < 7:
        for idx, row in enumerate(characters):
            print(f"{idx + 1}. {row['name']}")
        
        seleccion = input("Número del integrante (0 para terminar): ").strip()
        
        if seleccion == '0':
            break
        
        if not seleccion.isdigit():
            print("Entrada no válida. Debes ingresar un número.")
            continue
        
        seleccion = int(seleccion) - 1
        if 0 <= seleccion < len(characters):
            integrante_fila = characters[seleccion]
            # Verificar si el integrante ya ha sido agregado
            if not any(integrante.nombre == integrante_fila['name'] for integrante in integrantes):
                integrante = Integrante(integrante_fila['id'], integrante_fila['name'], integrante_fila['species'], integrante_fila['gender'])
                integrantes.append(integrante)
                print(f"Integrante {integrante.nombre} agregado.")
            else:
                print("Este integrante ya ha sido seleccionado. Por favor, elige otro.")
        else:
            print("Selección no válida. Por favor, selecciona un número válido.")

    # Crear la misión
    mision = Mision(nombre, planeta_seleccionado, nave_seleccionada, armas, integrantes)
    print("\nMisión creada con éxito:")
    print(mision)

    return mision


def modificar_mision(mision, planets, starships, weapons, characters):
    while True:
        print(f"\nModificando misión: {mision.nombre}")
        print("1. Modificar nombre")
        print("2. Modificar planeta")
        print("3. Modificar nave")
        print("4. Modificar armas")
        print("5. Modificar integrantes")
        print("6. Regresar al menú principal de modificación")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nuevo_nombre = input("Nuevo nombre de la misión: ").strip()
            mision.nombre = nuevo_nombre
            print(f"Nombre cambiado a {nuevo_nombre}")
        elif opcion == "2":
            print("Selecciona un nuevo planeta:")
            for idx, row in enumerate(planets):
                print(f"{idx + 1}. {row['name']}")
            seleccion = input("Número del planeta: ").strip()
            if seleccion.isdigit() and 0 <= int(seleccion) - 1 < len(planets):
                planeta_fila = planets[int(seleccion) - 1]
                nuevo_planeta = PlanetaCSV(planeta_fila['id'], planeta_fila['name'], planeta_fila['climate'], planeta_fila['terrain'])
                mision.planeta = nuevo_planeta
                print(f"Planeta cambiado a {nuevo_planeta.nombre}")
            else:
                print("Selección no válida.")
        elif opcion == "3":
            print("Selecciona una nueva nave:")
            for idx, row in enumerate(starships):
                print(f"{idx + 1}. {row['name']}")
            seleccion = input("Número de la nave: ").strip()
            if seleccion.isdigit() and 0 <= int(seleccion) - 1 < len(starships):
                nave_fila = starships[int(seleccion) - 1]
                nueva_nave = Nave(nave_fila['id'], nave_fila['name'], nave_fila['model'], nave_fila['manufacturer'], nave_fila['starship_class'], nave_fila['crew'])
                mision.nave = nueva_nave
                print(f"Nave cambiada a {nueva_nave.nombre}")
            else:
                print("Selección no válida.")
        elif opcion == "4":  # Modificar armas
            while True:
                print("Modificar armas:")
                print(f"Armas actuales ({len(mision.armas)}/7):")
                for idx, arma in enumerate(mision.armas):
                    print(f"{idx + 1}. {arma.nombre}")

                print("1. Agregar arma")
                print("2. Eliminar arma")
                print("3. Regresar")

                opcion_arma = input("Selecciona una opción: ")
                if opcion_arma == "1":
                    if len(mision.armas) < 7:
                        for idx, row in enumerate(weapons):
                            print(f"{idx + 1}. {row['name']}")
                        seleccion = input("Número del arma: ").strip()
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
                    seleccion = input("Número del arma a eliminar: ").strip()
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
                print("Modificar integrantes:")
                print(f"Integrantes actuales ({len(mision.integrantes)}/7):")
                for idx, integrante in enumerate(mision.integrantes):
                    print(f"{idx + 1}. {integrante.nombre}")

                print("1. Agregar integrante")
                print("2. Eliminar integrante")
                print("3. Regresar")

                opcion_integrante = input("Selecciona una opción: ")
                if opcion_integrante == "1":
                    if len(mision.integrantes) < 7:
                        for idx, row in enumerate(characters):
                            print(f"{idx + 1}. {row['name']}")
                        seleccion = input("Número del integrante: ").strip()
                        if seleccion.isdigit() and 0 <= int(seleccion) - 1 < len(characters):
                            integrante_fila = characters[int(seleccion) - 1]
                            if not any(integrante.nombre == integrante_fila['name'] for integrante in mision.integrantes):
                                nuevo_integrante = Integrante(integrante_fila['id'], integrante_fila['name'], integrante_fila['species'], integrante_fila['gender'])
                                mision.integrantes.append(nuevo_integrante)
                                print(f"Integrante agregado: {nuevo_integrante.nombre}")
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

def modificar_mision_detalle(misiones, planets, starships, weapons, characters):
    if not misiones:
        print("No hay misiones disponibles para modificar.")
        return

    while True:
        print("Selecciona una misión para modificar:")
        for idx, m in enumerate(misiones):
            print(f"{idx + 1}. {m.nombre}")
        
        seleccion = input("Número de la misión que deseas modificar: ").strip()

        if not seleccion.isdigit():
            print("Entrada no válida. Debes ingresar un número.")
            continue
        
        seleccion = int(seleccion) - 1

        if 0 <= seleccion < len(misiones):
            mision = misiones[seleccion]
            modificar_mision(mision, planets, starships, weapons, characters)
            break
        else:
            print("Selección no válida. Por favor, selecciona un número dentro del rango.")

def eliminar_mision(misiones):
    if not misiones:
        print("No hay misiones disponibles para eliminar.")
        return

    while True:
        print("Selecciona una misión para eliminar:")
        for idx, m in enumerate(misiones):
            print(f"{idx + 1}. {m.nombre}")
        
        seleccion = input("Número de la misión que deseas eliminar: ").strip()

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

def ver_mision_detalle(misiones):
    if not misiones:
        print("No hay misiones disponibles para ver.")
        return

    while True:
        print("Selecciona una misión para ver los detalles:")
        for idx, m in enumerate(misiones):
            print(f"{idx + 1}. {m.nombre}")
        
        seleccion = input("Número de la misión que deseas ver: ").strip()

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

def main():
    characters, planets, starships, weapons = cargar_datos()
    
    misiones = []
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            if len(misiones) >= 5:
                print("No puedes crear más de 5 misiones.")
            else:
                mision = crear_mision(planets, starships, weapons, characters, misiones)
                if mision:
                    misiones.append(mision)
        elif opcion == "2":
            modificar_mision_detalle(misiones, planets, starships, weapons, characters)
        elif opcion == "3":  # Ver misiones
            ver_mision_detalle(misiones)
        elif opcion == "4":
            nombre_archivo = input("Nombre del archivo para guardar las misiones: ")
            with open(nombre_archivo, 'w') as file:
                for mision in misiones:
                    file.write(mision.__str__() + "\n\n")
            print(f"Misiones guardadas en {nombre_archivo}")
        elif opcion == "5":
            nombre_archivo = input("Nombre del archivo para cargar las misiones: ")
            misiones_cargadas = Mision.cargar_de_archivo(nombre_archivo)  # Cargar las misiones desde el archivo
            if misiones_cargadas:
                misiones.extend(misiones_cargadas)  # Agregar las misiones cargadas a la lista existente
                print("Misiones cargadas con éxito.")
            else:
                print("No se pudieron cargar misiones.")
        elif opcion == "6":
            eliminar_mision(misiones)
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
