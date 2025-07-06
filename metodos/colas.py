from fastapi.exceptions import HTTPException
from fastapi import status
import matplotlib.pyplot as mlp
import seaborn as sns
import matplotlib
import math

def colear_mostrar(): 
    pass

def colear(Lambda : float, mu : float):
    try: 
        rho = Lambda / mu
        L = (Lambda ** 2) / (mu * (mu - Lambda))
        Lq = L + rho
        W = L / Lambda
        Wq = Lq / Lambda
        return {'rho': rho, 'L': L, 'Lq': Lq, 'W': W, 'Wq': Wq}
    except: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Los datos son incorrectos'
        )

def colear_probabilidad(llegada : float, servicio : float, clientes : float, espera : float, mayores : int): 
    try: 
        rho = llegada / servicio
        Pn = (1 - rho) * (rho ** clientes)
        PEspera = math.exp(-1 * (servicio - llegada) * espera)
        Pplus = rho ** (mayores + 1)
        return {'Pn': Pn, 'PEspera': PEspera, 'Pplus': Pplus}
    except: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Los datos son incorrectos'
        )