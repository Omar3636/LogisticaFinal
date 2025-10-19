import mysql.connector
import os
from src.app.modelos.envio import Envio

# Configuración de la conexión a Base de Datos
config = {
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'host': os.environ.get('MYSQL_HOST'),
    "port": os.environ.get('MYSQL_PORT'),
    'database': os.environ.get('MYSQL_DATABASE'),
}

# Crear una conexión
conexion = mysql.connector.connect(**config)

def agregar_bd(envio):
    cursor = None
    try:
        cursor = conexion.cursor()
        query = """
                INSERT INTO envios (proveedor, cliente, destino, estado, numero_seguimiento, fecha_entrega, fecha_ingreso)\
                VALUES (%(proveedor)s, %(cliente)s, %(destino)s, %(estado)s, %(numero_seguimiento)s, %(fecha_entrega)s, %(fecha_ingreso)s)
                """
        valores = envio.a_dicc()
        cursor.execute(query, valores)
        conexion.commit()
        print("Se ha agregado el registro con éxito en la base de datos.")
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error al agregar el envío a la base de datos: {str(e)}")
        conexion.rollback()
    finally:
        if cursor:
            cursor.close()

def buscar_bd(id):
    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        query = """ SELECT * FROM envios WHERE id = %s"""
        cursor.execute(query, (id,))
        envio_dicc = cursor.fetchone()
        if envio_dicc:
            return Envio.desde_dicc(envio_dicc)  # ← Convertir a objeto Envio
        else:
            return None
    except Exception as e:
        print(f"Error al buscar por ID el envío en base de datos: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()

def eliminar_bd(id):
    cursor = None
    try:
        cursor = conexion.cursor()
        query = "DELETE FROM envios WHERE id = %s"
        cursor.execute(query, (id,))
        conexion.commit()
        print("Se ha eliminado el registro en la base de datos con exito.")
    except Exception as e:
        print(f"Error al eliminar de base de datos: {e}")
        conexion.rollback()
    finally:
        if cursor:
            cursor.close()

def actualizar_bd(envio):
    cursor = None
    try:
        cursor = conexion.cursor()
        query = """
                UPDATE envios \
                SET proveedor = %(proveedor)s, \
                    cliente = %(cliente)s, \
                    destino = %(destino)s, \
                    estado = %(estado)s, \
                    numero_seguimiento = %(numero_seguimiento)s, \
                    fecha_entrega = %(fecha_entrega)s \
                WHERE id = %(id)s
                """
        valores = envio.a_dicc()
        cursor.execute(query, valores)
        conexion.commit()

        print(f"El envío con ID: {envio.id}, ha sido actualizado con exito en la base de datos.")
    except Exception as e:
        print(f"Error al actualizar envío en la base de datos: {str(e)}")
        conexion.rollback()
    finally:
        if cursor:
            cursor.close()

def mostrar_todo_bd():
    cursor = None
    try:
        cursor = conexion.cursor()
        query = "SELECT * FROM envios"
        cursor.execute(query)
        resultados = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        # Convertir cada fila a un objeto Envio
        lista_envios = []
        for fila in resultados:
            # Crear diccionario con nombres de columnas
            envio_dict = dict(zip(column_names, fila))
            # Convertir a objeto Envio
            envio = Envio.desde_dicc(envio_dict)
            lista_envios.append(envio)

        return lista_envios
    except Exception as e:
        print(f"Error al recuperar todos los envíos de la base de datos: {str(e)}")
        return []
    finally:
        if cursor:
            cursor.close()