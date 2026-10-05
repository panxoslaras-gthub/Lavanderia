class DAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()
