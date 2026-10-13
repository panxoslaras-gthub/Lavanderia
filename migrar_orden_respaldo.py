from conectar import crear_conexion


def migrar_orden_respaldo() -> None:
    conexion = crear_conexion()

    try:
        conexion.execute("BEGIN IMMEDIATE")

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS orden_respaldo_nueva (
                num_orden INTEGER PRIMARY KEY AUTOINCREMENT,
                num_boleta TEXT NOT NULL DEFAULT '',
                datos_json TEXT NOT NULL,
                registrada_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        tabla_actual = conexion.execute("""
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table' AND name = 'orden_respaldo'
        """).fetchone()

        if tabla_actual:
            conexion.execute("""
                INSERT INTO orden_respaldo_nueva (
                    num_orden,
                    num_boleta,
                    datos_json,
                    registrada_en
                )
                SELECT
                    num_orden,
                    num_boleta,
                    datos_json,
                    registrada_en
                FROM orden_respaldo
            """)
            conexion.execute("DROP TABLE orden_respaldo")

        conexion.execute("""
            ALTER TABLE orden_respaldo_nueva
            RENAME TO orden_respaldo
        """)

        conexion.commit()
        print("Tabla orden_respaldo preparada para generar folios automáticos.")

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


if __name__ == "__main__":
    migrar_orden_respaldo()