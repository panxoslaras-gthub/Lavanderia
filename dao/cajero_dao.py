from dao.empleado_dao import EmpleadoDAO

class CajeroDAO(EmpleadoDAO):
    def crear_tabla(self) -> None:
        cursor = self.conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cajero (
                id_empleado INTEGER PRIMARY KEY,
                password TEXT NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
            )
        """)
        self.conexion.commit()
        
    def autenticar(self,id_empleado: int, password_ingresada: str) -> bool:
        query = "SELECT password FROM cajero WHERE id_empleado = ?"
        cursor = self.conexion.cursor()
        cursor.execute(query, (id_empleado,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0] == password_ingresada
        return False
