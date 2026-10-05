from model.prenda import Prenda

class DetalleOrden: # Define la clase DetalleOrden para cada línea de prendas en la orden
    def __init__(self, prenda: Prenda, cantidad: int):
        self.__prenda: Prenda = prenda # Referencia al objeto Prenda
        self.cantidad = cantidad # Cantidad de prendas validada
        # Eliminamos la línea de self.__subtotal que generaba redundancia

    @property
    def prenda(self) -> Prenda: # Getter para la prenda
        return self.__prenda

    @property
    def cantidad(self) -> int: # Getter para la cantidad
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None: # Setter con validación de cantidad positiva
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("La cantidad de prendas debe ser un número entero mayor a 0.")
        self.__cantidad: int = valor

    @property
    def subtotal(self) -> float: # Getter para el subtotal
        return self.calcular_subtotal()

    def calcular_subtotal(self) -> float: # Calcula el subtotal multiplicando costo unitario por cantidad
        costo_unitario = self.__prenda.calcular_costo()
        # Retornamos el cálculo directamente sin guardarlo en una variable
        return round(costo_unitario * self.__cantidad, 2)

    def calcularSubtotal(self) -> float: # Alias camelCase según diagrama UML
        return self.calcular_subtotal()

    def __str__(self) -> str:
        return f"DetalleOrden({self.__cantidad}x {self.__prenda} = ${self.subtotal:,.0f} CLP)"
