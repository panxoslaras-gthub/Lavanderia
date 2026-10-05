from dao.dao import DAO
from model.cliente import Cliente
from typing import List, Optional

class ClienteDAO(DAO):
    def crear_tabla(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente (
                rut TEXT PRIMARY KEY
            )
        """)

    def insertar(self, cliente: Cliente) -> None:
        self.cursor.execute("INSERT OR REPLACE INTO cliente (rut) VALUES (?)", (cliente.rut,))
        self.conexion.commit()

        
    def obtener_por_rut(self, rut: str) -> Optional[Cliente]:
        self.cursor.execute("SELECT rut FROM cliente WHERE rut = ?", (rut.strip().upper(),))
        row = self.cursor.fetchone()
        if row:
            return Cliente(row[0])
        return None

    def listar_todos(self) -> List[Cliente]:
        self.cursor.execute("SELECT rut FROM cliente")
        return [Cliente(row[0]) for row in self.cursor.fetchall()]
