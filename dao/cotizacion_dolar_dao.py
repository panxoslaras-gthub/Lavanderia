from dao.dao import DAO

class CotizacionDolarDAO(DAO):
    def crear_tabla(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cotizacion_dolar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                valor_dolar REAL NOT NULL
            )
        """)
