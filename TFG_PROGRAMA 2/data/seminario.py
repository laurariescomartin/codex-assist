import pyodbc
from datetime import datetime

import pyodbc

def conectar_bd():
    try:
        conexion = pyodbc.connect(
            "DRIVER={MariaDB ODBC 3.2 Driver};" 
            "SERVER=localhost;"                 
            "PORT=3306;"                        
            "DATABASE=GyMarginadas;"  
            "UID=root;"                         
            "PWD=iissi$root;"                   
        )
        print("Conexión a la base de datos establecida.")
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

conexion = conectar_bd()
if conexion:
    conexion.close()

def crear_tablas_y_datos(conexion):
    puntero = conexion.puntero()
    try:
        puntero.execute("DROP TABLE IF EXISTS Stock, Pedido, Detalle_Pedido")
        
        puntero.execute("""
            CREATE TABLE Stock (
                Cproducto INT PRIMARY KEY,
                Cantidad INT
            )
        """)
        puntero.execute("""
            CREATE TABLE Pedido (
                Cpedido INT PRIMARY KEY,
                Ccliente INT,
                Fecha_pedido DATE
            )
        """)
        puntero.execute("""
            CREATE TABLE Detalle_Pedido (
                Cpedido INT,
                Cproducto INT,
                Cantidad INT,
                PRIMARY KEY (Cpedido, Cproducto),
                FOREIGN KEY (Cpedido) REFERENCES Pedido(Cpedido),
                FOREIGN KEY (Cproducto) REFERENCES Stock(Cproducto)
            )
        """)
        puntero.execute("DELETE FROM Stock")
        for i in range(10):
            puntero.execute("INSERT INTO Stock (Cproducto, Cantidad) VALUES (?, ?)", (i + 1, 100))
        conexion.commit()
        print("Las tablas han sido creadas y los datos iniciales insertados correctamente.")
    except Exception as e:
        conexion.rollback()
        print("Error al crear las tablas o al insertar los datos:", e)

def alta_pedido(conexion):
    puntero = conexion.puntero()
    try:
        cpedido = int(input("Código del pedido: "))
        ccliente = int(input("Código del cliente: "))
        fecha_pedido = datetime.now().strftime('%Y-%m-%d')
        puntero.execute("INSERT INTO Pedido (Cpedido, Ccliente, Fecha_pedido) VALUES (?, ?, ?)",
                       (cpedido, ccliente, fecha_pedido))
        puntero.execute("SAVEPOINT pedido_creado")
        print(f"Pedido {cpedido} creado.")

        while True:
            print("\nOpciones para el pedido:")
            print("1. Añadir detalle del producto")
            print("2. Eliminar todos los detalles del producto")
            print("3. Cancelar el pedido")
            print("4. Finalizar el pedido")
            opcion = input("Seleccione una opción, por favor: ")

            if opcion == "1":
                cproducto = int(input("Código del producto: "))
                cantidad = int(input("Cantidad: "))
                puntero.execute("SELECT Cantidad FROM Stock WHERE Cproducto = ?", (cproducto,))
                stock = puntero.fetchone()
                if stock and stock[0] >= cantidad:
                    puntero.execute("INSERT INTO Detalle_Pedido (Cpedido, Cproducto, Cantidad) VALUES (?, ?, ?)",
                                   (cpedido, cproducto, cantidad))
                    puntero.execute("UPDATE Stock SET Cantidad = Cantidad - ? WHERE Cproducto = ?",
                                   (cantidad, cproducto))
                    print(f"Producto {cproducto} añadido al pedido {cpedido}.")
                else:
                    print("Stock insuficiente para este producto.")
            elif opcion == "2":
                puntero.execute("DELETE FROM Detalle_Pedido WHERE Cpedido = ?", (cpedido,))
                print("Todos los detalles del pedido han sido eliminados.")
            elif opcion == "3":
                puntero.execute("ROLLBACK TO pedido_creado")
                puntero.execute("DELETE FROM Pedido WHERE Cpedido = ?", (cpedido,))
                print(f"Pedido {cpedido} cancelado.")
                break
            elif opcion == "4":
                conexion.commit()
                print(f"El pedido {cpedido} fue finalizado correctamente.")
                break
            else:
                print("La opción no válida.")
            mostrar_tablas(conexion)
    except Exception as e:
        conexion.rollback()
        print("Ha habido un error al gestionar el pedido:", e)


def mostrar_tablas(conexion):
    puntero = conexion.puntero()
    try:
        for tabla in ["Stock", "Pedido", "Detalle_Pedido"]:
            print(f"\nContenido de la tabla {tabla}:")
            puntero.execute(f"SELECT * FROM {tabla}")
            filas = puntero.fetchall()
            for fila in filas:
                print(fila)
    except Exception as e:
        print("Error al mostrar las tablas:", e)


def menu_principal(conexion):
    while True:
        print("\nMenú Principal:")
        print("1. Crear tablas y datos iniciales")
        print("2. Dar de alta un nuevo pedido")
        print("3. Mostrar contenido de las tablas")
        print("4. Salir del programa")
        opcion = input("Seleccione una opción, por favor: ")

        if opcion == "1":
            crear_tablas_y_datos(conexion)
        elif opcion == "2":
            alta_pedido(conexion)
        elif opcion == "3":
            mostrar_tablas(conexion)
        elif opcion == "4":
            conexion.close()
            print("Conexión cerrada. Hasta pronto!!.")
            break
        else:
            print("La opción no es válida. Intentalo de nuevo porfavor.")

if __name__ == "__main__":
    conexion = conectar_bd()
    if conexion:
        menu_principal(conexion)