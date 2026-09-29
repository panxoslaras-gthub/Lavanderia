class DAO:
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = conexion.cursor()
