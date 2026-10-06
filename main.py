from datetime import date
from conectar import crear_conexion
from servicios.miindicador import MiIndicador

# Importación de DAOs
from dao.cliente_dao import ClienteDAO
from dao.empleado_dao import EmpleadoDAO
from dao.cajero_dao import CajeroDAO
from dao.operario_dao import OperarioDAO
from dao.maquina_dao import MaquinaDAO
from dao.producto_quimico_dao import ProductoQuimicoDAO
from dao.cotizacion_dolar_dao import CotizacionDolarDAO
from dao.ropa_normal_dao import RopaNormalDAO
from dao.alfombra_dao import AlfombraDAO
from dao.edredon_cobertor_dao import EdredonCobertorDAO
from dao.orden_dao import OrdenDAO
from dao.detalle_orden_dao import DetalleOrdenDAO

# Importación de Modelos de Dominio
from model.cliente import Cliente
from model.cajero import Cajero
from model.operario import Operario
from model.maquina import Maquina
from model.cotizacion_dolar import CotizacionDolar
from model.producto_quimico import ProductoQuimico
from model.ropa_normal import RopaNormal
from model.alfombra import Alfombra
from model.edredon_cobertor import EdredonCobertor
from model.detalle_orden import DetalleOrden
from model.orden import Orden


def solicitar_entero_positivo(mensaje: str) -> int:
    while True:
        try:
            val = int(input(mensaje).strip())
            if val > 0:
                return val
            print("Error: Ingrese un número entero positivo mayor a 0.")
        except ValueError:
            print("Error: Entrada inválida. Debe ingresar un número entero.")


def solicitar_rut() -> str:
    while True:
        rut_str = input("Ingrese el RUT del cliente (con puntos y guion): ").strip()
        try:
            cliente_temp = Cliente(rut=rut_str)
            if cliente_temp.validar_rut():
                return rut_str
            else:
                print("Formato invalido. Intente de nuevo (RECUERDA: ingresar rut con puntos y guion.")
        except ValueError as e:
            print(f"Error: {e}")


def main():
    print("================================================================")
    print("           SISTEMA DE GESTIÓN DE LAVANDERÍA INTERACTIVO")
    print("================================================================")

    # 1. GESTIÓN DE BASE DE DATOS Y TABLAS
    print("\n[1] Inicializando base de datos y tablas mediante capa DAO...")
    conexion = crear_conexion()

    cliente_dao = ClienteDAO(conexion)
    cajero_dao = CajeroDAO(conexion)
    operario_dao = OperarioDAO(conexion)
    maquina_dao = MaquinaDAO(conexion)
    prod_quimico_dao = ProductoQuimicoDAO(conexion)
    cotizacion_dao = CotizacionDolarDAO(conexion)
    ropa_dao = RopaNormalDAO(conexion)
    alfombra_dao = AlfombraDAO(conexion)
    edredon_dao = EdredonCobertorDAO(conexion)
    orden_dao = OrdenDAO(conexion)
    detalle_dao = DetalleOrdenDAO(conexion)

    cliente_dao.crear_tabla()
    cajero_dao.crear_tabla()
    operario_dao.crear_tabla()
    maquina_dao.crear_tabla()
    prod_quimico_dao.crear_tabla()
    cotizacion_dao.crear_tabla()
    ropa_dao.crear_tabla()
    alfombra_dao.crear_tabla()
    edredon_dao.crear_tabla()
    orden_dao.crear_tabla()
    detalle_dao.crear_tabla()

    conexion.commit()
    print("-> ¡Tablas verificadas e inicializadas en 'lavanderia.db'!")

    # 2. COTIZACIÓN DEL DÓLAR
    print("\n[2] Obteniendo la cotización actual del Dólar...")
    try:
        indicador_service = MiIndicador()
        valor_dolar_api = indicador_service.obtener_valor("dolar")
        print(f"-> Cotización obtenida desde mindicador.cl API: ${valor_dolar_api:,.2f} CLP")
    except Exception as e:
        valor_dolar_api = 945.50
        print(f"-> No se pudo conectar a la API ({e}). Usando valor por defecto: ${valor_dolar_api:,.2f} CLP")

    cotizacion = CotizacionDolar(fecha=date.today(), valor_dolar=valor_dolar_api)

    # Insumos químicos base
    detergente_bio = ProductoQuimico(nombre="Detergente Enzimático Bio", precio_dolar=4.50)
    solvente_seco = ProductoQuimico(nombre="Solvente Percloroetileno Puro", precio_dolar=8.20)
    desmanchador = ProductoQuimico(nombre="Desmanchador Alcalino Pro", precio_dolar=6.00)

    # 3. REGISTRO INTERACTIVO DE PERSONAL Y MAQUINARIAS
    print("\n[3] Registro de Personal y Maquinarias")
    id_cajero = solicitar_entero_positivo("Ingrese ID del Cajero a cargo: ")
    cajero = Cajero(id_empleado=id_cajero)

    id_operario = solicitar_entero_positivo("Ingrese ID del Operario a cargo: ")
    operario = Operario(id_empleado=id_operario)

    cant_maquinas = solicitar_entero_positivo("Ingrese la cantidad de máquinas a asignar al operario: ")
    for i in range(1, cant_maquinas + 1):
        id_maq = solicitar_entero_positivo(f"  - Ingrese el ID para la Máquina #{i}: ")
        maquina = Maquina(id_maquina=id_maq)
        operario.asignar_maquina(maquina)

    print(f"-> Personal registrado:")
    print(f"   * {cajero}")
    print(f"   * {operario} (Máquinas asignadas: {[m.id_maquina for m in operario.maquinas_asignadas]})")

    # 4. REGISTRO INTERACTIVO DE CLIENTE Y ORDEN DE SERVICIO
    print("\n[4] Creación de Orden de Servicio")
    rut_cliente = solicitar_rut()
    cliente = Cliente(rut=rut_cliente)
    cliente_dao.insertar(cliente)

    num_orden = solicitar_entero_positivo("Ingrese el Número de Orden (ej. 1001): ")
    num_boleta = input("Ingrese el Número de Boleta (ej. B-2026-0001): ").strip()

    cajero.recibir_prendas()
    cajero.registrar_orden()

    # 5. INGRESO DE PRENDAS
    detalles = []
    print("\n[5] Ingreso de Prendas para la Orden")
    while True:
        print("\n--- Selección de Tipo de Prenda ---")
        print("1. Ropa Normal (Camisa, Traje, Pantalón, etc.)")
        print("2. Alfombra")
        print("3. Edredón / Cobertor")
        opcion_prenda = input("Seleccione el tipo de prenda (1-3): ").strip()

        print("\n--- Estado de la Prenda ---")
        print("Estados válidos: sucio, delicado, manchado, regular")
        estado = input("Ingrese el estado de la prenda: ").strip().lower()

        if opcion_prenda == "1":
            lavado_seco_input = input("¿Requiere Lavado al Seco? (s/n): ").strip().lower()
            lavado_seco = (lavado_seco_input == 's')
            quimico = solvente_seco if lavado_seco else detergente_bio
            prenda_obj = RopaNormal(estado_inicial=estado, lavado_seco=lavado_seco, producto_quimico=quimico)
        elif opcion_prenda == "2":
            prenda_obj = Alfombra(estado_inicial=estado, lavado_seco=False, producto_quimico=desmanchador)
        elif opcion_prenda == "3":
            lavado_seco_input = input("¿Requiere Lavado al Seco? (s/n): ").strip().lower()
            lavado_seco = (lavado_seco_input == 's')
            quimico = solvente_seco if lavado_seco else detergente_bio
            prenda_obj = EdredonCobertor(estado_inicial=estado, lavado_seco=lavado_seco, producto_quimico=quimico)
        else:
            print("Opción inválida. Intente de nuevo.")
            continue

        cantidad = solicitar_entero_positivo(f"Ingrese la cantidad de prendas para {prenda_obj.__class__.__name__}: ")
        detalle = DetalleOrden(prenda=prenda_obj, cantidad=cantidad)
        detalles.append(detalle)

        continuar = input("\n¿Desea agregar otra prenda a esta orden? (s/n): ").strip().lower()
        if continuar != 's':
            break

    # Construcción de la Orden completa
    orden = Orden(
        num_orden=num_orden,
        num_boleta=num_boleta,
        cliente=cliente,
        cajero=cajero,
        detalles=detalles,
        pagada=False
    )

    print("\n================================================================")
    print(f" RESUMEN DE LA ORDEN #{orden.num_orden} - BOLETA {orden.num_boleta}")
    print("================================================================")
    print(f"Cliente RUT: {orden.cliente.rut}")
    print(f"Cajero a cargo ID: {orden.cajero.id_empleado}")
    print("Prendas ingresadas:")
    for d in orden.detalles:
        print(f"   * {d}")

    total_orden = orden.calcular_total()
    print(f"\n-> TOTAL A PAGAR: ${total_orden:,.0f} CLP")

    # 6. PROCESO DE OPERACIÓN Y PAGO INTERACTIVO
    print("\n[6] Procesamiento en Planta y Lavado")
    for d in orden.detalles:
        operario.procesar_prenda(d.prenda)

    if operario.maquinas_asignadas:
        operario.operar_maquina(operario.maquinas_asignadas[0])

    print("\nIntentando entregar la orden antes de cobrar:")
    orden.entregar_orden()

    input("\nPresione [ENTER] para proceder al cobro y pago de la orden...")
    cajero.cobrar_orden()
    orden.pagar()
    print(f"-> Estado de pago verificado: {orden.verificar_pago()}")

    print("\nEntregando prendas tras la verificación del pago:")
    orden.entregar_orden()
    cajero.entregar_prendas()

    conexion.close()
    print("\n================================================================")
    print("     EJECUCIÓN DEL SISTEMA COMPLETADA EXITOSAMENTE")
    print("================================================================")


if __name__ == "__main__":
    main()

