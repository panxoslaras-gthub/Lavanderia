from model.prenda import Prenda
from model.producto_quimico import ProductoQuimico

class RopaNormal(Prenda): # Define la subclase RopaNormal que hereda de Prenda
    def __init__(self, estado_inicial: str, lavado_seco: bool, producto_quimico: ProductoQuimico):
        super().__init__(estado_inicial, lavado_seco, producto_quimico)

    def calcular_costo(self) -> float: # Sobrescribe el cálculo de costo base para prendas comunes
        costo_base = 3500.0
        if self.lavado_seco:
            costo_base += 1500.0
        return costo_base

    def calcularCosto(self) -> float: # Alias camelCase según diagrama UML
        return self.calcular_costo()

    def calcular_tiempo_lavado(self) -> int: # Retorna el tiempo en minutos para ropa normal
        return 40 if not self.lavado_seco else 60

    def calcularTiempoLavado(self) -> int: # Alias camelCase según diagrama UML
        return self.calcular_tiempo_lavado()

    def __str__(self) -> str:
        tipo = "Seco" if self.lavado_seco else "Agua"
        return f"RopaNormal(Estado: {self.estado_inicial}, Lavado: {tipo})"
