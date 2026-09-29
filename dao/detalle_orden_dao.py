from dao.dao import DAO

class DetalleOrdenDAO(DAO):
    def crear_tabla(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_orden (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_orden INTEGER NOT NULL,
                prenda_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (num_orden) REFERENCES orden(num_orden),
                FOREIGN KEY (prenda_id) REFERENCES prenda(id)
            )
        """)
