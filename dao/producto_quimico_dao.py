from dao.dao import DAO

class ProductoQuimicoDAO(DAO):
    def crear_tabla(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS producto_quimico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio_dolar REAL NOT NULL
            )
        """)
