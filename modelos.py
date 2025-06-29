from pydantic import BaseModel

class datos_form_abc(BaseModel): 
    visiones: str
    archivo: str
    nombres: str
    costos: str
    demandas: str

class datos_form_descuentos(BaseModel): 
    pass

class dato_form_lote(BaseModel):
    pass

class dato_form_probabilistico(BaseModel): 
    pedido: float
    almacenamiento: float
    acumulado: float
    promedio: float
    laborales: float
    desviacion: float
    perdida: float