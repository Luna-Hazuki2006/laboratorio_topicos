from pydantic import BaseModel
from enum import Enum

class datos_form_abc(BaseModel): 
    visiones: str
    archivo: str
    nombres: str
    costos: str
    demandas: str

class datos_form_descuentos(BaseModel): 
    pass

class Medidas(Enum): 
    dias = 'dias'
    semanas = 'semanas'
    meses = 'meses'
    anual = 'anual'

class datos_form_economico(BaseModel): 
    unitario : float
    demanda : float
    pedido : float
    almacenamiento : float
    entrega : float
    medida : Medidas
    perdida : float

DESCUENTOS = ['unidades', 'descuentos', 'almacenamiento', 'preparacion']

class dato_form_cola(BaseModel): 
    llegada : float
    servicio : float
    clientes : float
    espera : float
    mayores : float

class dato_form_probabilistico(BaseModel): 
    pedido: float
    almacenamiento: float
    acumulado: float
    promedio: float
    laborales: float
    desviacion: float
    perdida: float