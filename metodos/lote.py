from fastapi import status
from fastapi.exceptions import HTTPException
import matplotlib.pyplot as plt
import matplotlib
import math

def lotear(unitario : float, demanda : float, pedido : float, almacenamiento : float, entrega : float): 
    if any(valor <= 0 for valor in [unitario, demanda, pedido, almacenamiento, entrega]): 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Todos los datos tienen que ser mayores a 0'
        )
    Q = math.sqrt((2 * pedido * demanda) / almacenamiento)
    T = Q / demanda
    R = -1
    m = 0
    if T / entrega: 
        R =  demanda * entrega
    else: 
        while R == -1: 
            if (entrega - m * T) > 0 and (entrega - (m + 1) * T) < 0: R = demanda * (entrega - m * T)
            else: m += 1
    C = (unitario * demanda) + (demanda / Q) + (0.5 * almacenamiento * Q) 
    return {'hola': 'mundo'}