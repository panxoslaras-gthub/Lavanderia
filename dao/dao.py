class DAO:
    def __init__(self, conexion):
        self.__conexion = conexion
        self.__cursor = conexion.cursor()

    @property
    def conexion(self):
        return self.__conexion

    @property
    def cursor(self):
        return self.__cursor


