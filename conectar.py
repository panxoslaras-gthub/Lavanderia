import sqlite3
import os
DB_PATH= os.path.join(os.path.dirname(os.path.abspath(__file__)),"lavanderia.db")
def crear_conexion():
    """Crea y retorna una conexion a la base de datosSQLite."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        conexion.execute("PRAGMA foreing_keys = ON")
        return conexion
    except sqlite3.Error as e:
        print(F"Error al conectar con la base de datos:{e}")
        raise
