import sqlite3

def crear_conexion():
    conexion = sqlite3.connect("lavanderia.db")
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion
