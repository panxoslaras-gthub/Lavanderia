from dao.dao import DAO

class PrendaDAO(DAO):
    def crear_tabla(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS prenda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                estado_inicial TEXT NOT NULL,
                lavado_seco INTEGER NOT NULL,
                producto_quimico_id INTEGER NOT NULL,
                FOREIGN KEY (producto_quimico_id) REFERENCES producto_quimico(id)
            )
        """)
