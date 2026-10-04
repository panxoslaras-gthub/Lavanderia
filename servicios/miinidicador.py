import requests

class MiIndicador:
    BASE_URL ="https://mindicador.cl/api/"

    def __init__(self, timeout=5):
        self.__timeout=timeout

    def obtener_valor(self, codigo, fecha=None):
        url= self.BASE_URL + codigo
        if fecha:
            url += f"/{fecha}"
            
        respuesta = requests.get(url, timeout=self.__timeout)
        datos = respuesta.json()
        
        if not datos.get("serie"):
            raise ValueError("No se encontraron valores para el indicador en la fecha proporcionada.")
            
        return datos["serie"][0]["valor"]