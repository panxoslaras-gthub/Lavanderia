from dao.dao import DAO
import json
from model.orden import Orden
from model.operario import Operario

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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orden_respaldo (
                num_orden INTEGER PRIMARY KEY AUTOINCREMENT,
                num_boleta TEXT NOT NULL DEFAULT '',
                datos_json TEXT NOT NULL,
                registrada_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def guardar_respaldo(
        self,
        orden: Orden,
        fecha: str,
        operario: Operario,
        tiempo_lavado: int,
    ) -> None:
        datos = {
            "num_orden": None,
            "num_boleta": "",
            "fecha": fecha,
            "cliente_rut": orden.cliente.rut,
            "cajero_id": orden.cajero.id_empleado,
            "operario_id": operario.id_empleado,
            "detalles": [
                {
                    "tipo": type(detalle.prenda).__name__,
                    "estado": detalle.prenda.estado_inicial,
                    "lavado_seco": detalle.prenda.lavado_seco,
                    "producto_quimico": detalle.prenda.producto_quimico.nombre,
                    "cantidad": detalle.cantidad,
                    "subtotal": detalle.calcular_subtotal(),
                }
                for detalle in orden.detalles
            ],
            "tiempo_lavado": tiempo_lavado,
            "maquinas": [
                maquina.id_maquina
                for maquina in operario.maquinas_asignadas
            ],
            "total": orden.calcular_total(),
            "estado": "En Proceso",
        }

        try:
            cursor = self.conexion.cursor()
            cursor.execute(
                """
                INSERT INTO orden_respaldo (num_boleta, datos_json)
                VALUES (?, ?)
                """,
                ("", "{}"),
            )

            orden.num_orden = cursor.lastrowid
            datos["num_orden"] = orden.num_orden

            cursor.execute(
                """
                UPDATE orden_respaldo
                SET datos_json = ?
                WHERE num_orden = ?
                """,
                (
                    json.dumps(datos, ensure_ascii=False),
                    orden.num_orden,
                ),
            )

            self.conexion.commit()

        except Exception:
            self.conexion.rollback()
            raise
