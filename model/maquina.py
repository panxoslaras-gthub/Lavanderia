class Maquina: # Define la clase Maquina para representar el equipo de lavado
    def __init__(self, id_maquina: int): # Constructor que recibe el identificador de la máquina
        self.id_maquina = id_maquina # Asigna mediante setter para validar

    @property
    def id_maquina(self) -> int: # Getter que permite acceder al idMaquina privado
        return self.__id_maquina

    @id_maquina.setter
    def id_maquina(self, valor: int) -> None: # Setter para validar id positivo
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El idMaquina debe ser un entero positivo mayor a 0.")
        self.__id_maquina: int = valor

    @property
    def idMaquina(self) -> int: # Alias camelCase según diagrama UML
        return self.id_maquina

    def iniciar_lavado(self) -> None: # Método para iniciar el ciclo de lavado en la máquina
        print(f"Máquina #{self.__id_maquina}: Ciclo de lavado iniciado.")

    def iniciarLavado(self) -> None: # Alias camelCase según diagrama UML
        self.iniciar_lavado()

    def __str__(self) -> str:
        return f"Maquina(idMaquina={self.__id_maquina})"
