from model.empleado import Empleado

class Cajero(Empleado): # Define la clase Cajero heredando de Empleado
    def __init__(self, id_empleado, password=""): # Constructor que recibe el id del cajero
        super().__init__(id_empleado) # Llama al constructor de la clase base Empleado
        self.password = password
        
    @property
    def password(self):
            return self._password

    @password.setter
    def password(self, value):
        if len(value) < 4:
            raise ValueError("por seguridad, la contraseña debe tener al menos 4 caracteres.")
        self._password = value
        
    def recibir_prendas(self) -> None: # Método para registrar la recepción de prendas del cliente
        print(f"Cajero #{self.id_empleado} ha recibido las prendas del cliente.")

    def recibirPrendas(self) -> None: # Alias camelCase según diagrama UML
        self.recibir_prendas()

    def registrar_orden(self) -> None: # Método para formalizar una nueva orden de servicio
        print(f"Cajero #{self.id_empleado} ha registrado la orden en el sistema.")

    def registrarOrden(self) -> None: # Alias camelCase según diagrama UML
        self.registrar_orden()

    def cobrar_orden(self) -> None: # Método para efectuar el cobro de la orden
        print(f"Cajero #{self.id_empleado} ha procesado el cobro de la orden.")

    def cobrarOrden(self) -> None: # Alias camelCase según diagrama UML
        self.cobrar_orden()

    def entregar_prendas(self) -> bool: # Método para realizar la entrega de prendas lavadas
        print(f"Cajero #{self.id_empleado} entrega las prendas finalizadas.")
        return True

    def entregarPrendas(self) -> bool: # Alias camelCase según diagrama UML
        return self.entregar_prendas()

    def __str__(self) -> str:
        return f"Cajero(idEmpleado={self.id_empleado})"
