class ProductoQuimico: # Define la clase ProductoQuimico para insumos de lavado
    def __init__(self, nombre: str, precio_dolar: float): # Constructor con nombre y precio en dólares
        self.nombre = nombre # Nombre del producto químico
        self.precio_dolar = precio_dolar # Precio en USD validado

    @property
    def nombre(self) -> str: # Getter para nombre
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None: # Setter con validación para nombre no vacío
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto químico no puede estar vacío.")
        self.__nombre: str = valor.strip()

    @property
    def precio_dolar(self) -> float: # Getter para precioDolar
        return self.__precio_dolar

    @precio_dolar.setter
    def precio_dolar(self, valor: float) -> None: # Setter con validación para precio positivo
        if valor < 0:
            raise ValueError("El precio en dólares no puede ser negativo.")
        self.__precio_dolar: float = float(valor)

    @property
    def precioDolar(self) -> float: # Alias camelCase según diagrama UML
        return self.precio_dolar

    def calcular_precio_pesos(self, valor_dolar: float) -> float: # Método para calcular el costo en CLP
        if valor_dolar <= 0:
            raise ValueError("El valor del dólar debe ser mayor a 0.")
        return round(self.__precio_dolar * valor_dolar, 2)

    def calcularPrecioPesos(self, valorDolar: float) -> float: # Alias camelCase según diagrama UML
        return self.calcular_precio_pesos(valorDolar)

    def __str__(self) -> str:
        return f"ProductoQuimico({self.__nombre}, USD ${self.__precio_dolar:.2f})"
