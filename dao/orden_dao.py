from dao.dao import DAO

class OrdenDAO(DAO):
    def crear_tabla(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orden (
                num_orden INTEGER PRIMARY KEY,
                num_boleta TEXT NOT NULL,
                pagada INTEGER NOT NULL,
                cliente_rut TEXT NOT NULL,
                cajero_id INTEGER NOT NULL,
                FOREIGN KEY (cliente_rut) REFERENCES cliente(rut),
                FOREIGN KEY (cajero_id) REFERENCES cajero(id_empleado)
            )
        """)
