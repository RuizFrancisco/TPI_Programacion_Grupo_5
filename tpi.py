import sqlite3
class Libreria:
    def __init__(self):
        self.conexion = Conexiones()
        self.conexion.abrirConexion()
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS LIBROS")
        self.conexion.miCursor.execute("CREATE TABLE LIBROS (id_libro INTEGER PRIMARY KEY AUTOINCREMENT, isbn INTEGER NOT NULL, titulo VARCHAR(30), autor VARCHAR(30), genero VARCHAR(30), precio FLOAT NOT NULL, fechaUltimoPrecio VARCHAR(30), cantidadDisponibles INTEGER NOT NULL, UNIQUE(isbn))")
        self.conexion.miConexion.commit()
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS VENTAS")
        #self.conexion.miCursor.execute("CREATE TABLE VENTAS (id_libro INTEGER PRIMARY KEY AUTOINCREMENT, cantidadDisponibles INTEGER NOT NULL, fechaVenta VARCHAR(30)")
        self.conexion.miConexion.execute("CREATE TABLE VENTAS (id_libro INTEGER, cantidadVenta INTEGER NOT NULL, fechaVenta VARCHAR(30), FOREIGN KEY (id_libro) REFERENCES LIBROS(id_libro));")
        self.conexion.miConexion.commit()
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS HISTORICO_LIBROS")
        self.conexion.miCursor.execute("CREATE TABLE HISTORICO_LIBROS (id_libro INTEGER, precio FLOAT NOT NULL, fechaUltimoPrecio VARCHAR(30), FOREIGN KEY (id_libro, precio, fechaUltimoPrecio) REFERENCES LIBROS(id_libro, precio, fechaUltimoPrecio))")
        self.conexion.miConexion.commit()
    
    #funciones extras
    def validar_id(self, id_libro):
        self.conexion.miCursor.execute("SELECT id_libro FROM LIBROS")
        resultados = self.conexion.miCursor.fetchall()
        for fila in resultados:
            if id_libro == fila[0]:
                return True    
        return False

    def hacer_linea(self):
        print("----------------------")

    #1
    def agregar_libro(self, isbn, titulo, autor, genero, precio, fechaUltimoPrecio, cantidadDisponibles):
        try:
            self.conexion.miCursor.execute("INSERT INTO LIBROS (isbn, titulo, autor, genero, precio, fechaUltimoPrecio, cantidadDisponibles) VALUES (?, ?, ?, ?, ?, ?, ?)", (isbn, titulo, autor, genero, precio, fechaUltimoPrecio, cantidadDisponibles))
            self.conexion.miConexion.commit()
            print("Libro agregado exitosamente")
        except:
            print("Error al agregar un libro")

    #2
    def modificar_libro(self, id_libro, precio):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET precio = ? WHERE id_libro = ?", (precio, id_libro))
            self.conexion.miConexion.commit()
            print("Libro modificado correctamente")
        except:
            print("Error al modificar el libro")

    #3
    def borrar_libro(self, id_libro):
        try:
            self.conexion.miCursor.execute("DELETE FROM LIBROS WHERE id_libro = ?", (id_libro))
            self.conexion.miConexion.commit()
            print("Libro borrado correctamente")
        except:
            print("Error al borrar el libro")

    #4
    def incrementar_cantidad(self, id_libro, cantidadDisponibles):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET cantidadDisponibles = ? WHERE id_libro = ?", (cantidadDisponibles, id_libro))
            self.conexion.miConexion.commit()
            print("Cantidad del libro incrementada correctamente")
        except:
            print("Error al incrementar cantidad del libro")
    
    #5
    def listarlibros(self, orden):
        try:
            if orden == "1":
                self.conexion.miCursor.execute("SELECT * FROM LIBROS ORDER BY id_libro ASC")
            elif orden == "2":
                self.conexion.miCursor.execute("SELECT * FROM LIBROS ORDER BY autor ASC")
            elif orden == "3":
                self.conexion.miCursor.execute("SELECT * FROM LIBROS ORDER BY titulo ASC")
            resultados = self.conexion.miCursor.fetchall()

            # Encabezados de las columnas
            encabezados = ["ID", "ISBN", "Título", "Autor", "Genero", "Precio", "Fecha", "Cantidad"]

            # Datos de ejemplo
            datos = resultados 

            # Longitud máxima de cada columna
            longitudes = [max(len(str(dato)) for dato in columna) for columna in zip(encabezados, *datos)]

            # Línea separadora
            linea_separadora = ''.join('-' * (longitud + 2) for longitud in longitudes)

            # Imprimir encabezados
            print(linea_separadora)
            print("\t\t\tTABLA DE LIBROS")
            print(linea_separadora)
            print('|', end='')
            for encabezado, longitud in zip(encabezados, longitudes):
                print(f' {encabezado:{longitud}s} |', end='')
            print()
            print(linea_separadora)

            # Imprimir datos
            for fila in datos:
                print('|', end='')
                for dato, longitud in zip(fila, longitudes):
                    print(f' {dato:{longitud}} |', end='')
                print()

            print(linea_separadora)

        except:
            print("Error al listar los libros")

    #6
    def agregar_venta(self, id_libro, cantidadVenta, fechaVenta):
        try:
            self.conexion.miCursor.execute("INSERT INTO VENTAS (id_libro, cantidadVenta, fechaVenta) VALUES (?, ?, ?)", (id_libro, cantidadVenta, fechaVenta))
            self.conexion.miConexion.commit()
            print("Venta agregada exitosamente")

            self.conexion.miCursor.execute("SELECT * FROM VENTAS")
            resultados = self.conexion.miCursor.fetchall()

            # Encabezados de las columnas
            encabezados = ["ID", "Cantidad Vendidos", "Fecha Venta"]

            # Datos de ejemplo
            datos = resultados 

            # Longitud máxima de cada columna
            longitudes = [max(len(str(dato)) for dato in columna) for columna in zip(encabezados, *datos)]

            # Línea separadora
            linea_separadora = ''.join('-' * (longitud + 2) for longitud in longitudes)

            # Imprimir encabezados
            print(linea_separadora)
            print("\t\tTABLA DE VENTAS")
            print(linea_separadora)
            print('|', end='')
            for encabezado, longitud in zip(encabezados, longitudes):
                print(f' {encabezado:{longitud}s} |', end='')
            print()
            print(linea_separadora)

            # Imprimir datos
            for fila in datos:
                print('|', end='')
                for dato, longitud in zip(fila, longitudes):
                    print(f' {dato:{longitud}} |', end='')
                print()

            print(linea_separadora)
        except:
            print("Error al agregar una venta")

    def descontar_cantidad(self, id_libro, cantidadDisponibles):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET cantidadDisponibles = ? WHERE id_libro = ?", (cantidadDisponibles, id_libro))
            self.conexion.miConexion.commit()
            print("Cantidad descontada correctamente")
        except:
            print("Error al descontar cantidad de un libro")

    #7
    def insertar_historico(self):
        try:
            self.conexion.miCursor.execute("INSERT INTO HISTORICO_LIBROS (id_libro, precio, fechaUltimoPrecio) SELECT id_libro, precio, fechaUltimoPrecio FROM LIBROS")
            self.conexion.miConexion.commit()
            print("Historico actualizado exitosamente")

            self.conexion.miCursor.execute("SELECT * FROM HISTORICO_LIBROS")
            resultados = self.conexion.miCursor.fetchall()

            # Encabezados de las columnas
            encabezados = ["ID", "Precio", "Fecha Ultimo Precio"]

            # Datos de ejemplo
            datos = resultados 

            # Longitud máxima de cada columna
            longitudes = [max(len(str(dato)) for dato in columna) for columna in zip(encabezados, *datos)]

            # Línea separadora
            linea_separadora = ''.join('-' * (longitud + 2) for longitud in longitudes)

            # Imprimir encabezados
            print(linea_separadora)
            print("\tTABLA HISTORICO LIBROS")
            print(linea_separadora)
            print('|', end='')
            for encabezado, longitud in zip(encabezados, longitudes):
                print(f' {encabezado:{longitud}s} |', end='')
            print()
            print(linea_separadora)

            # Imprimir datos
            for fila in datos:
                print('|', end='')
                for dato, longitud in zip(fila, longitudes):
                    print(f' {dato:{longitud}} |', end='')
                print()

            print(linea_separadora)
        except:
            print("Error al actualizar el historico")

    def actualizar_precio(self, porcentaje, fechaUltimoPrecio):
        try:
            self.conexion.miCursor.execute("SELECT * FROM LIBROS")
            resultados = self.conexion.miCursor.fetchall()

            for fila in resultados:
                precio = fila[5]
                precio = precio + (precio * (porcentaje/100))
                id_libro = fila[0]
                self.conexion.miCursor.execute("UPDATE LIBROS SET precio = ?, fechaUltimoPrecio = ? WHERE id_libro = ?", (precio, fechaUltimoPrecio, id_libro))
                self.conexion.miConexion.commit()
            
            print("Se actualizaron los precios correctamente")
        except:
            print("Error al actualizar los precios de los libros")

    #8
    def registros_anteriores(self, fechaMenu8):
        try:
            self.conexion.miCursor.execute("SELECT * FROM HISTORICO_LIBROS ORDER BY fechaUltimoPrecio ASC")
            resultados = self.conexion.miCursor.fetchall()
            for fila in resultados:
                if fila[2] < fechaMenu8:
                    print(fila)
            print("Los registros se obtuvieron correctamente")
        except:
            print("Error al obtener los registros")

    #0
    def cerrar_libreria(self):
        self.conexion.cerrarConexion()

class Conexiones:
    def abrirConexion(self):
        self.miConexion = sqlite3.connect("Libreria.db")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()  


libreria = Libreria()

while True:
    print("Menu de opciones Libreria.")
    print("1- Agregar libro.")
    print("2- Modificar precio de un libro.")
    print("3- Borrar un libro.")
    print("4- Cargar disponibilidad.")
    print("5- Listado de Libros.")
    print("6- Ventas.")
    print("7- Actualizar precios.")
    print("8- Mostrar registros anteriores a fecha ingresada.")
    print("0- Salir del menú.")
    
    opcion = int(input("Por favor ingrese un número: "))
    
    if opcion == 1:
        isbn = int(input("Por favor ingrese el ISBN del libro : "))
        while isbn <= 0:
            isbn = int(input("¡ERROR! Ingrese el ISBN del libro (mayor a 0): "))
        titulo = input("Por favor ingrese el título del libro: ").capitalize()
        autor = input("Por favor ingrese el autor del libro: ").capitalize()
        genero = input("Por favor ingrese el genero del libro: ").capitalize()
        precio = float(input("Por favor ingrese el precio del libro: "))
        while precio <= 0:
            precio = float(input("¡ERROR! Ingrese el precio del libro (mayor a 0): "))
        fechaUltimoPrecio = input("Por favor ingrese la fecha del ultimo precio del libro: ")
        cantidadDisponibles = int(input("Por favor ingrese la cantidad de unidades disponibles: "))
        while cantidadDisponibles <= 0:
            cantidadDisponibles = int(input("¡ERROR! Ingrese la cantidad de unidades disponibles (mayor a 0): "))
        libreria.agregar_libro(isbn, titulo, autor, genero, precio, fechaUltimoPrecio, cantidadDisponibles)
        libreria.hacer_linea()

    elif opcion == 2:
        id_libro = int(input("Por favor ingrese el ID del libro a modificar: "))
        while id_libro <= 0:
            id_libro = int(input("¡ERROR! Ingrese el ID del libro a modificar (mayor a 0): "))

        validacion = libreria.validar_id(id_libro)
        if validacion:
            precio = float(input("Por favor ingrese el nuevo precio del libro: "))
            while precio <= 0:
                precio = float(input("¡ERROR! Ingrese el nuevo precio del libro (mayor a 0): "))
            resp = input("Confirma que quiere actualizar el precio (S/N): ")
            while resp != "S" and resp != "s" and resp != "N" and resp != "n":
                resp = input("Ingreso mal su respuesta vuelva a ingresarla (S/N): ")
            if resp == "S" or resp == "s":
                libreria.modificar_libro(id_libro, precio)
            elif resp == "N" or resp == "n":
                print("Se canceló la accion")
        else:
            print("ID no encontrado")
        
        libreria.hacer_linea()

    elif opcion == 3:
        id_libro = int(input("Por favor ingrese el ID del quiere borrar: "))
        while id_libro <= 0:
            id_libro = int(input("¡ERROR! Ingrese el ID del libro a eliminar (mayor a 0): "))
        validacion = libreria.validar_id(id_libro)
        if validacion:
            resp = input("Confirma que quiere borrar el libro (S/N): ")
            while resp != "S" and resp != "s" and resp != "N" and resp != "n":
                resp = input("Ingreso mal su respuesta vuelva a ingresarla (S/N): ")
            if resp == "S" or resp == "s":
                libreria.borrar_libro(id_libro)
            elif resp == "N" or resp == "n":
                print("Se canceló la accion")
        else:
            print("ID no encontrado")
        libreria.hacer_linea()

    elif opcion == 4:
        id_libro = int(input("Por favor ingrese el ID del libro al cual le quiere cargar su disponibilidad: "))
        while id_libro <= 0:
            id_libro = int(input("¡ERROR! Ingrese el ID del libro al cual le quiere cargar su disponibilidad (mayor a 0): "))
        validacion = libreria.validar_id(id_libro)
        if validacion:
            cantidadDisponibles += int(input("Ingrese la cantidad de libros a agregar: "))
            while cantidadDisponibles <= 0:
                cantidadDisponibles += int(input("¡ERROR! Ingrese la cantidad de libros a agregar (mayor a 0): "))
            libreria.incrementar_cantidad(id_libro, cantidadDisponibles)
        else:
            print("ID no encontrado")
        libreria.hacer_linea()

    elif opcion == 5:
        print("Menu de opciones para mostrar ordenadamente:") 
        print("1- Mostrar por ID")
        print("2- Mostrar por autor")
        print("3- Mostrar por titulo")
        print("0- Salir del menú")
        
        orden = int(input("Por favor ingrese el criterio de orden (ID/Autor/Titulo): "))
        while orden < 0 or orden > 3:
            orden= int(input("¡ERROR! Ingrese una opcion valida: "))
        libreria.listarlibros(orden)

    elif opcion == 6:
        id_libro = int(input("Ingrese el id del libro vendido: "))
        while id_libro <= 0:
            id_libro = int(input("¡ERROR! Ingrese el id del libro vendido(mayor a 0): "))
        validacion = libreria.validar_id(id_libro)
        if validacion:
            cantidadVenta = int(input("Ingrese la cantidad de libros vendidos: "))
            while cantidadVenta <= 0:
                cantidadVenta = int(input("¡ERROR! Ingrese la cantidad de libros vendidos: "))
            if cantidadDisponibles >= cantidadVenta:
                cantidadDisponibles -= cantidadVenta
                fechaVenta = input("Ingrese la fecha en la que se realizo la venta: ")
                libreria.agregar_venta(id_libro, cantidadVenta, fechaVenta)
                libreria.descontar_cantidad(id_libro, cantidadDisponibles)
            else:
                print("El stock es menor a la cantidad de libros vendidos")
        else:
            print("ID no encontrado")

        libreria.hacer_linea()
    
    elif opcion == 7:
        libreria.insertar_historico()
        porcentaje = float(input("Ingrese el porcentaje del aumento/disminucion (100 = 100%): "))
        fechaUltimoPrecio = input("Ingrese la fecha del cambio: ")
        libreria.actualizar_precio(porcentaje, fechaUltimoPrecio)
        libreria.hacer_linea()
    
    elif opcion == 8:
        fechaMenu8 = input("Ingrese un fecha para mostrar sus registros anteriores: ")
        libreria.registros_anteriores(fechaMenu8)
        libreria.hacer_linea()

    elif opcion == 0:
        libreria.cerrar_libreria()
        break

    else:
        print("¡Ingreso opcion no valida!")
        libreria.hacer_linea()
