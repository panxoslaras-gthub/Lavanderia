import requests

class MiIndicador:
    BASE_URL = "https://mindicador.cl/api/"

    def __init__(self, timeout=5):
        self.__timeout = timeout

    def obtener_valor(self, codigo, fecha=None):
        url = self.BASE_URL + codigo
        if fecha:
            url += f"/{fecha}"

        try:
            respuesta = requests.get(url, timeout=self.__timeout)
            
            respuesta.raise_for_status()
            
            datos = respuesta.json()

            if not datos.get("serie"):
                raise ValueError("No se encontraron valores para el indicador en la fecha proporcionada.")

            return datos["serie"][0]["valor"]

        except requests.exceptions.HTTPError as error_http:
            print(f"Disculpe, tuvimos un problema de comunicación con la página de indicadores: {error_http}")
            raise error_http
        except requests.exceptions.RequestException as error_conexion:
            print(f"Hubo un problema de conexión al intentar obtener los datos: {error_conexion}")
            raise error_conexion

