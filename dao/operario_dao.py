from dao.empleado_dao import EmpleadoDAO

class OperarioDAO(EmpleadoDAO):
    def crear_tabla(self) -> None:
        super().crear_tabla()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS operario (
                id_empleado INTEGER PRIMARY KEY,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
            )
        """)
