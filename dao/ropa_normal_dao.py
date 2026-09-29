from dao.prenda_dao import PrendaDAO

class RopaNormalDAO(PrendaDAO):
    def crear_tabla(self) -> None:
        super().crear_tabla()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ropa_normal (
                prenda_id INTEGER PRIMARY KEY,
                FOREIGN KEY (prenda_id) REFERENCES prenda(id)
            )
        """)
