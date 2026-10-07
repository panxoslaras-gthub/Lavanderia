from typing import List, Optional
from model.cliente import Cliente
from model.cajero import Cajero
from model.detalle_orden import DetalleOrden

class Orden: # Define la clase Orden para gestionar el pedido de servicio
    def __init__(
        self,
        num_orden: int,
        num_boleta: str,
        cliente: Cliente,
        cajero: Cajero,
        detalles: Optional[List[DetalleOrden]] = None,
        pagada: bool = False
    ):
        self.num_orden = num_orden
        self.num_boleta = num_boleta
        self.__cliente: Cliente = cliente
        self.__cajero: Cajero = cajero
        self.__detalles: List[DetalleOrden] = detalles if detalles is not None else []
        self.__pagada: bool = bool(pagada)

    @property
    def num_orden(self) -> int: # Getter para numOrden
        return self.__num_orden

    @num_orden.setter
    def num_orden(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("El número de orden debe ser un número entero.")
        if valor <= 0:
            raise ValueError("El número de orden debe ser un entero entre 1 y 999.999.999.")
        self.__num_orden = valor

    @property
    def numOrden(self) -> int: # Alias camelCase según diagrama UML
        return self.num_orden

    @property
    def num_boleta(self) -> str: # Getter para numBoleta
        return self.__num_boleta

    @num_boleta.setter
    def num_boleta(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("El número de boleta debe ser texto.")
        self.__num_boleta = valor.strip()

    @property
    def numBoleta(self) -> str: # Alias camelCase según diagrama UML
        return self.num_boleta

    @property
    def pagada(self) -> bool: # Getter para pagada
        return self.__pagada

    @property
    def cliente(self) -> Cliente: # Getter para cliente
        return self.__cliente

    @property
    def cajero(self) -> Cajero: # Getter para cajero
        return self.__cajero

    @property
    def detalles(self) -> List[DetalleOrden]: # Getter para detalles
        return self.__detalles

    def agregar_detalle(self, detalle: DetalleOrden) -> None: # Método auxiliar para agregar ítems a la orden
        self.__detalles.append(detalle)

    def validar_identificacion(self) -> bool: # Valida que cliente y cajero existan y cliente tenga RUT válido
        if self.__cliente is None or self.__cajero is None:
            return False
        return self.__cliente.validar_rut()

    def validarIdentificacion(self) -> bool: # Alias camelCase según diagrama UML
        return self.validar_identificacion()

    def calcular_total(self) -> float: # Suma los subtotales de todos los detalles asociados
        total = sum(d.calcular_subtotal() for d in self.__detalles)
        return round(total, 2)

    def calcularTotal(self) -> float: # Alias camelCase según diagrama UML
        return self.calcular_total()

    def verificar_pago(self) -> bool: # Verifica si la orden se encuentra debidamente pagada
        return self.__pagada

    def verificarPago(self) -> bool: # Alias camelCase según diagrama UML
        return self.verificar_pago()

    def pagar(self) -> None: # Método de conveniencia para registrar el pago
        self.__pagada = True

    def entregar_orden(self) -> bool: # Entrega la orden solo si se encuentra pagada
        if not self.verificar_pago():
            print(f"Error: La orden #{self.__num_orden} no puede entregarse porque no ha sido pagada.")
            return False
        print(f"Éxito: La orden #{self.__num_orden} ha sido entregada al cliente {self.__cliente.rut}.")
        return True

    def entregarOrden(self) -> bool: # Alias camelCase según diagrama UML
        return self.entregar_orden()

    def __str__(self) -> str:
        estado = "PAGADA" if self.__pagada else "PENDIENTE"
        return f"Orden #{self.__num_orden} [Boleta: {self.__num_boleta}] - Cliente: {self.__cliente.rut} - Total: ${self.calcular_total():,.0f} CLP ({estado})"
