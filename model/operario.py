from typing import List, Optional
from model.empleado import Empleado
from model.maquina import Maquina
from model.prenda import Prenda

class Operario(Empleado): # Define la clase Operario que hereda de Empleado
    def __init__(self, id_empleado: int, maquinas_asignadas: Optional[List[Maquina]] = None):
        super().__init__(id_empleado)
        self.__maquinas_asignadas: List[Maquina] = maquinas_asignadas if maquinas_asignadas is not None else []

    @property
    def maquinas_asignadas(self) -> List[Maquina]: # Getter para la lista de máquinas asignadas
        return self.__maquinas_asignadas

    @property
    def maquinasAsignadas(self) -> List[Maquina]: # Alias camelCase según diagrama UML
        return self.maquinas_asignadas

    def asignar_maquina(self, maquina: Maquina) -> None: # Método auxiliar para asignar una máquina
        if maquina not in self.__maquinas_asignadas:
            self.__maquinas_asignadas.append(maquina)

    def asignarMaquina(self, maquina: Maquina) -> None: # Alias camelCase según diagrama UML
        self.asignar_maquina(maquina)


    def procesar_prenda(self, prenda: Prenda) -> None: # Método para procesar y preparar la prenda
        print(f"Operario #{self.id_empleado} procesando prenda {prenda}...")
        print(f"  -> Tiempo estimado de lavado: {prenda.calcular_tiempo_lavado()} minutos.")

    def procesarPrenda(self, prenda: Prenda) -> None: # Alias camelCase según diagrama UML
        self.procesar_prenda(prenda)

    def operar_maquina(self, maquina: Maquina) -> None: # Método para operar una máquina asignada
        print(f"Operario #{self.id_empleado} operando la máquina #{maquina.id_maquina}.")
        maquina.iniciar_lavado()

    def operarMaquina(self, maquina: Maquina) -> None: # Alias camelCase según diagrama UML
        self.operar_maquina(maquina)

    def __str__(self) -> str:
        return f"Operario(idEmpleado={self.id_empleado}, maquinas={len(self.__maquinas_asignadas)})"
