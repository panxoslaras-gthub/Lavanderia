from dao.dao import DAO

class MaquinaDAO(DAO):
    def crear_tabla(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS maquina (
                id_maquina INTEGER PRIMARY KEY AUTOINCREMENT
            )
        """)
