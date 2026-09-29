from datetime import date

class CotizacionDolar: # Define la clase CotizacionDolar para la tasa cambiaria
    def __init__(self, fecha: date, valor_dolar: float): # Constructor con fecha y valor del dólar
        self.__fecha: date = fecha # Atributo privado fecha
        self.valor_dolar = valor_dolar # Atributo privado valor_dolar validado en el setter

    @property
    def fecha(self) -> date: # Getter para fecha
        return self.__fecha

    @property
    def valor_dolar(self) -> float: # Getter para valor_dolar
        return self.__valor_dolar

    @valor_dolar.setter
    def valor_dolar(self, valor: float) -> None: # Setter con validación para valor positivo
        if valor <= 0:
            raise ValueError("El valor del dólar debe ser mayor a 0.")
        self.__valor_dolar: float = float(valor)

    @property
    def valorDolar(self) -> float: # Alias camelCase según diagrama UML
        return self.valor_dolar

    def obtener_valor_dolar(self) -> float: # Método para consultar el valor actual del dólar
        return self.__valor_dolar

    def obtenerValorDolar(self) -> float: # Alias camelCase según diagrama UML
        return self.obtener_valor_dolar()

    def __str__(self) -> str:
        return f"CotizacionDolar({self.__fecha}: ${self.__valor_dolar:.2f} CLP)"
