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

        self.cursor.execute("""
            INSERT INTO sqlite_sequence (name, seq)
            SELECT 'orden_respaldo', 100
            WHERE NOT EXISTS (
                SELECT 1 FROM sqlite_sequence
                WHERE name = 'orden_respaldo'
            )
        """)
        self.cursor.execute("""
            UPDATE sqlite_sequence
            SET seq = MAX(seq, 100)
            WHERE name = 'orden_respaldo'
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

    def obtener_respaldo(self, num_orden: int) -> dict | None:
        fila = self.conexion.execute(
            """
            SELECT num_boleta, datos_json
            FROM orden_respaldo
            WHERE num_orden = ?
            """,
            (num_orden,),
        ).fetchone()

        if fila is None:
            return None

        datos = json.loads(fila[1])
        datos["num_orden"] = num_orden
        datos["num_boleta"] = fila[0]
        return datos

    def actualizar_estado(self, num_orden: int, nuevo_estado: str) -> None:
        datos = self.obtener_respaldo(num_orden)
        if datos is None:
            raise ValueError(f"No existe la orden {num_orden}.")

        transiciones = {
            "En Proceso": "Listo Para Entrega",
            "Listo Para Entrega": "Pagada_Cerrada",
        }
        estado_esperado = transiciones.get(datos["estado"])

        if nuevo_estado != estado_esperado:
            raise ValueError(
                f"Transición inválida: {datos['estado']} -> {nuevo_estado}."
            )

        datos["estado"] = nuevo_estado
        self.conexion.execute(
            """
            UPDATE orden_respaldo
            SET datos_json = ?
            WHERE num_orden = ?
            """,
            (json.dumps(datos, ensure_ascii=False), num_orden),
        )
        self.conexion.commit()

    def asignar_num_boleta(self, num_orden: int) -> str:
        try:
            self.conexion.execute("BEGIN IMMEDIATE")

            fila = self.conexion.execute(
                """
                SELECT num_boleta, datos_json
                FROM orden_respaldo
                WHERE num_orden = ?
                """,
                (num_orden,),
            ).fetchone()

            if fila is None:
                raise ValueError(f"No existe la orden {num_orden}.")

            if fila[0]:
                self.conexion.commit()
                return fila[0]

            mayor_boleta = self.conexion.execute("""
                SELECT MAX(CAST(num_boleta AS INTEGER))
                FROM orden_respaldo
                WHERE num_boleta <> ''
                  AND num_boleta NOT GLOB '*[^0-9]*'
            """).fetchone()[0]

            num_boleta = str(max(mayor_boleta or 900, 900) + 1)
            datos = json.loads(fila[1])
            datos["num_boleta"] = num_boleta

            self.conexion.execute(
                """
                UPDATE orden_respaldo
                SET num_boleta = ?, datos_json = ?
                WHERE num_orden = ?
                """,
                (
                    num_boleta,
                    json.dumps(datos, ensure_ascii=False),
                    num_orden,
                ),
            )
            self.conexion.commit()
            return num_boleta

        except Exception:
            self.conexion.rollback()
            raise