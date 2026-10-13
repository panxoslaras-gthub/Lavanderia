import getpass
from conectar import crear_conexion

id_empleado = int(input("ID del cajero (número positivo): ").strip())
if id_empleado <= 0:
    raise ValueError("El ID debe ser positivo.")

password = getpass.getpass("Nueva contraseña (mínimo 4 caracteres): ")
confirmacion = getpass.getpass("Confirma la contraseña: ")

if password != confirmacion:
    raise ValueError("Las contraseñas no coinciden.")
if len(password) < 4:
    raise ValueError("La contraseña debe tener al menos 4 caracteres.")

conexion = crear_conexion()
try:
    existe = conexion.execute(
        "SELECT 1 FROM cajero WHERE id_empleado = ?",
        (id_empleado,),
    ).fetchone()

    if existe:
        raise ValueError("Ese ID de cajero ya está registrado.")

    conexion.execute(
        "INSERT INTO cajero (id_empleado, password) VALUES (?, ?)",
        (id_empleado, password),
    )
    conexion.commit()
    print("Cajero registrado.")
finally:
    conexion.close()