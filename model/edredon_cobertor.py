from model.prenda import Prenda
from model.producto_quimico import ProductoQuimico

class EdredonCobertor(Prenda): # Define la subclase EdredonCobertor que hereda de Prenda
    def __init__(self, estado_inicial: str, lavado_seco: bool, producto_quimico: ProductoQuimico):
        super().__init__(estado_inicial, lavado_seco, producto_quimico)

    def calcular_costo(self) -> float: # Sobrescribe costo para edredones y cobertores
        costo_base = 8500.0
        if self.lavado_seco:
            costo_base += 2500.0
        return costo_base

    def calcularCosto(self) -> float: # Alias camelCase según diagrama UML
        return self.calcular_costo()

    def calcular_tiempo_lavado(self) -> int: # Retorna tiempo en minutos para edredones
        return 70 if not self.lavado_seco else 85

    def calcularTiempoLavado(self) -> int: # Alias camelCase según diagrama UML
        return self.calcular_tiempo_lavado()

    def __str__(self) -> str:
        tipo = "Seco" if self.lavado_seco else "Agua"
        return f"EdredonCobertor(Estado: {self.estado_inicial}, Lavado: {tipo})"
