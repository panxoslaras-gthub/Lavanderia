from abc import ABC, abstractmethod
from model.producto_quimico import ProductoQuimico

class Prenda(ABC): # Define la clase abstracta base Prenda
    def __init__(self, estado_inicial: str, lavado_seco: bool, producto_quimico: ProductoQuimico):
        self.estado_inicial = estado_inicial # Estado inicial recibido de la prenda
        self.__lavado_seco: bool = bool(lavado_seco) # Booleano indicando si requiere lavado en seco
        self.__producto_quimico: ProductoQuimico = producto_quimico # Insumo químico asignado

    @property
    def estado_inicial(self) -> str: # Getter para estadoInicial
        return self.__estado_inicial

    @estado_inicial.setter
    def estado_inicial(self, valor: str) -> None: # Setter con validación
        if not valor or not valor.strip():
            raise ValueError("El estado inicial de la prenda no puede estar vacío.")
        self.__estado_inicial: str = valor.strip()

    @property
    def estadoInicial(self) -> str: # Alias camelCase según diagrama UML
        return self.estado_inicial

    @property
    def lavado_seco(self) -> bool: # Getter para lavadoSeco
        return self.__lavado_seco

    @property
    def lavadoSeco(self) -> bool: # Alias camelCase según diagrama UML
        return self.lavado_seco

    @property
    def producto_quimico(self) -> ProductoQuimico: # Getter para productoQuimico
        return self.__producto_quimico

    @property
    def productoQuimico(self) -> ProductoQuimico: # Alias camelCase según diagrama UML
        return self.producto_quimico

    def validar_estado(self) -> bool: # Valida que la prenda sea apta para el proceso de lavado
        estados_validos = ["bueno", "regular", "manchado", "delicado", "sucio"]
        return self.__estado_inicial.lower() in estados_validos

    def validarEstado(self) -> bool: # Alias camelCase según diagrama UML
        return self.validar_estado()

    @abstractmethod
    def calcular_costo(self) -> float: # Método abstracto para el costo polimórfico del lavado
        pass

    def calcularCosto(self) -> float: # Alias camelCase
        return self.calcular_costo()

    @abstractmethod
    def calcular_tiempo_lavado(self) -> int: # Método abstracto para el tiempo estimado en minutos
        pass

    def calcularTiempoLavado(self) -> int: # Alias camelCase
        return self.calcular_tiempo_lavado()
