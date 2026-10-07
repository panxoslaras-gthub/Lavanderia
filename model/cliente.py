import re

class Cliente: # Define la clase Cliente
    def __init__(self, rut: str): # Constructor que inicializa el RUT del cliente
        self.rut = rut # Asigna a través del setter para validar el formato

    @property
    def rut(self) -> str: # Getter para acceder al RUT privado
        return self.__rut

    @rut.setter
    def rut(self, valor: str) -> None: # Setter con validación de RUT chileno básico
        valor_limpio = valor.strip().replace(".", "").upper()
        if not re.match(r"^\d{7,8}-[\dK]$", valor_limpio):
            raise ValueError(f"Formato invalido del rut '{valor}'. Intente nuevamente (RECUERDA: ingresar guion y digito verificador.")
        self.__rut: str = valor_limpio

    def validar_rut(self) -> bool: # Método para verificar si el dígito verificador del RUT es correcto
        try:
            cuerpo, dv = self.__rut.split("-")
            suma = 0
            multiplo = 2
            for c in reversed(cuerpo):
                suma += int(c) * multiplo
                multiplo = 2 if multiplo == 7 else multiplo + 1
            esperado = 11 - (suma % 11)
            dv_esperado = "K" if esperado == 10 else ("0" if esperado == 11 else str(esperado))
            return dv == dv_esperado
        except Exception:
            return False

    def validarRut(self) -> bool: # Alias camelCase según diagrama UML
        return self.validar_rut()

    def __str__(self) -> str:
        return f"Cliente(RUT: {self.__rut})"
