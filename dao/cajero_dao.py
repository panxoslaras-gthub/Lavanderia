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
