from abc import ABC, abstractmethod

class Empleado(ABC): # Define la clase abstracta base Empleado
    def __init__(self, id_empleado: int): # Constructor que recibe el identificador del empleado
        self.id_empleado = id_empleado # Asigna mediante setter para validar

    @property
    def id_empleado(self) -> int: # Getter que permite acceder al idEmpleado privado
        return self.__id_empleado

    @id_empleado.setter
    def id_empleado(self, valor: int) -> None: # Setter con validación para asegurar id positivo
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El idEmpleado debe ser un número entero positivo mayor a 0.")
        self.__id_empleado: int = valor

    @property
    def idEmpleado(self) -> int: # Alias camelCase según diagrama UML
        return self.id_empleado

    def __str__(self) -> str:
        return f"Empleado #{self.__id_empleado}"
