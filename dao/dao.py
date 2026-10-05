class DAO:
    def __init__(self, conexion):
        self.__conexion = conexion
        self.__cursor = conexion.cursor()
