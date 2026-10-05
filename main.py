from datetime import date
from conectar import crear_conexion
# Importación del Servicio de Indicadores Económicos (API)
from servicios.miinidicador import MiIndicador

# Importación de DAOs
from dao.cliente_dao import ClienteDAO
from dao.empleado_dao import EmpleadoDAO
from dao.cajero_dao import CajeroDAO
from dao.operario_dao import OperarioDAO
from dao.maquina_dao import MaquinaDAO
from dao.producto_quimico_dao import ProductoQuimicoDAO
from dao.cotizacion_dolar_dao import CotizacionDolarDAO
from dao.prenda_dao import PrendaDAO
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

def main():
    print("================================================================")
    print("           SISTEMA DE GESTIÓN DE LAVANDERÍA")
    print("================================================================")

    # ------------------------------------------------------------------
    # 1. GESTIÓN DE BASE DE DATOS Y CREACIÓN DE TABLAS (CAPA DAO)
    # ------------------------------------------------------------------
    print("\n[1] Inicializando base de datos y tablas mediante capa DAO...")
    conexion = crear_conexion()

    # Instanciación de DAOs pasando la conexión compartida
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

    # Creación de tablas relacionales en orden de dependencias
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
    print("-> ¡Tablas creadas exitosamente en la base de datos 'lavanderia.db'!")

    # ------------------------------------------------------------------
    # 2. PRUEBA DE DOMINIO: INSUMOS QUÍMICOS Y COTIZACIÓN DEL DÓLAR (VÍA SERVICIO API)
    # ------------------------------------------------------------------
    print("\n[2] Configuración de cotización y cálculo de precios de insumos mediante API...")
    try:
        indicador_service = MiIndicador()
        valor_dolar_api = indicador_service.obtener_valor("dolar")
        print(f"-> Cotización del Dólar obtenida desde mindicador.cl API: ${valor_dolar_api:,.2f} CLP")
    except Exception as e:
        valor_dolar_api = 945.50
        print(f"-> No se pudo conectar a la API ({e}). Usando valor por defecto: ${valor_dolar_api:,.2f} CLP")

    cotizacion = CotizacionDolar(fecha=date.today(), valor_dolar=valor_dolar_api)
    print(f"-> {cotizacion}")

    detergente_bio = ProductoQuimico(nombre="Detergente Enzimático Bio", precio_dolar=4.50)
    solvente_seco = ProductoQuimico(nombre="Solvente Percloroetileno Puro", precio_dolar=8.20)
    desmanchador = ProductoQuimico(nombre="Desmanchador Alcalino Pro", precio_dolar=6.00)

    precio_pesos_detergente = detergente_bio.calcular_precio_pesos(cotizacion.obtener_valor_dolar())
    precio_pesos_solvente = solvente_seco.calcular_precio_pesos(cotizacion.obtener_valor_dolar())
    print(f"-> {detergente_bio.nombre}: USD ${detergente_bio.precio_dolar} = ${precio_pesos_detergente:,.0f} CLP")
    print(f"-> {solvente_seco.nombre}: USD ${solvente_seco.precio_dolar} = ${precio_pesos_solvente:,.0f} CLP")

    # ------------------------------------------------------------------
    # 3. PRUEBA DE PERSONAL Y MAQUINARIAS
    # ------------------------------------------------------------------
    print("\n[3] Instanciando personal y equipos...")
    cajero = Cajero(id_empleado=101)
    operario = Operario(id_empleado=202)
    lavadora_industrial_1 = Maquina(id_maquina=1)
    lavadora_industrial_2 = Maquina(id_maquina=2)

    operario.asignar_maquina(lavadora_industrial_1)
    operario.asignar_maquina(lavadora_industrial_2)
    print(f"-> {cajero}")
    print(f"-> {operario} (Máquinas asignadas: {[m.id_maquina for m in operario.maquinas_asignadas]})")

    # ------------------------------------------------------------------
    # 4. INSTANCIACIÓN DE PRENDAS (POLIMORFISMO Y HERENCIA)
    # ------------------------------------------------------------------
    print("\n[4] Recepción de prendas y aplicación de polimorfismo...")
    camisa = RopaNormal(estado_inicial="sucio", lavado_seco=False, producto_quimico=detergente_bio)
    traje = RopaNormal(estado_inicial="delicado", lavado_seco=True, producto_quimico=solvente_seco)
    alfombra_sala = Alfombra(estado_inicial="manchado", lavado_seco=False, producto_quimico=desmanchador)
    edredon_pluma = EdredonCobertor(estado_inicial="regular", lavado_seco=True, producto_quimico=solvente_seco)

    prendas = [camisa, traje, alfombra_sala, edredon_pluma]
    for p in prendas:
        print(f"   * {p.__class__.__name__}:")
        print(f"     - Estado apto: {p.validar_estado()}")
        print(f"     - Costo unitario de lavado: ${p.calcular_costo():,.0f} CLP")
        print(f"     - Tiempo de ciclo: {p.calcular_tiempo_lavado()} minutos")

    # ------------------------------------------------------------------
    # 5. GENERACIÓN DE ORDEN DE SERVICIO
    # ------------------------------------------------------------------
    print("\n[5] Registro y procesamiento de la Orden...")
    cliente = Cliente(rut="12345678-5")
    cajero.recibir_prendas()
    cajero.registrar_orden()

    detalle_1 = DetalleOrden(prenda=camisa, cantidad=3)
    detalle_2 = DetalleOrden(prenda=traje, cantidad=1)
    detalle_3 = DetalleOrden(prenda=alfombra_sala, cantidad=1)
    detalle_4 = DetalleOrden(prenda=edredon_pluma, cantidad=2)

    orden = Orden(
        num_orden=1001,
        num_boleta="B-2026-0089",
        cliente=cliente,
        cajero=cajero,
        detalles=[detalle_1, detalle_2, detalle_3, detalle_4],
        pagada=False
    )

    print(f"-> Identificación válida: {orden.validar_identificacion()}")
    print("\nDesglose de detalles:")
    for d in orden.detalles:
        print(f"   - {d}")

    total_orden = orden.calcular_total()
    print(f"\n-> TOTAL GENERAL ORDEN #{orden.num_orden}: ${total_orden:,.0f} CLP")

    # ------------------------------------------------------------------
    # 6. OPERACIÓN EN PLANTA Y ENTREGA FINAL
    # ------------------------------------------------------------------
    print("\n[6] Proceso de lavado y entrega al cliente...")
    for d in orden.detalles:
        operario.procesar_prenda(d.prenda)
    operario.operar_maquina(lavadora_industrial_1)

    print("\nIntentando entregar antes del pago:")
    orden.entregar_orden()

    print("\nProcesando cobro:")
    cajero.cobrar_orden()
    orden.pagar()
    print(f"-> Estado de pago verificado: {orden.verificar_pago()}")

    print("\nIntentando entregar tras el pago:")
    orden.entregar_orden()
    cajero.entregar_prendas()

    conexion.close()
    print("\n================================================================")
    print("     EJECUCIÓN DEL SISTEMA COMPLETADA EXITOSAMENTE")
    print("================================================================")

if __name__ == "__main__":
    main()
