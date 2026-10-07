from dao.empleado_dao import EmpleadoDAO

class CajeroDAO(EmpleadoDAO):
    def crear_tabla(self) -> None:
        super().crear_tabla()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cajero (
                id_empleado INTEGER PRIMARY KEY,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
            )
        """)
    def autenticar(self,id_empleado: int, password_ingresada: str) -> bool:
        query = "SELECT password FROM cajero WHERE id_empleado = ?"
        self.conexion.cursor().execute(query, (id_empleado,))
        resultado = self.conexion.cursor().fetchone()
        if resultado:
            password_bd = resultado[0]
            return password_bd == password_ingresada
        return False
