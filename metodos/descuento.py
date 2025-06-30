from fastapi.exceptions import HTTPException
from fastapi import UploadFile, status
from pandas import DataFrame
from pprint import pprint
import matplotlib.pylab as plt
import seaborn as sns
import matplotlib
import base64
import time
import csv
import os
import re

def lectura(dato : str): 
    return float(dato.replace(',', '.').strip())

def descontar(tabla : list[dict[str, str]], nombres : list[str], datos : dict[str, str | UploadFile]): 
    for i, cada in enumerate(tabla): 
        patron = r'^-?\d+([.,]\d+)?\s*-\s*-?\d+([.,]\d+)?$'
        rangos = cada[nombres[0]].split('-')
        if i == len(tabla) -1: 
            try: 
                if float(rangos[0].strip()) != 0 and rangos[1].strip().isalnum():
                    cada[nombres[0]].replace(rangos[1], str(999999999999999999999))
                elif float(rangos[0]) != 0 and float(rangos[1]) != 0: pass
                else: 
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail='Las únidades tienen que estar en un rango numérico, en vez de "49 - infinito" es mejor "49 - 999999"'
                    )
            except: 
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail='Todas las únidades tienen que estar en un rango, incluso la última fila, por ejemplo "49 - 999999""'
                )
        else: 
            if not re.fullmatch(patron, cada[nombres[0]]): 
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail='Las únidades tienen que estar en un rango'
                )
        if lectura(rangos[0]) > lectura(rangos[1]): 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail='Las únidades tienen que ir de menor a mayor'
            )
        for este in nombres[1:]: cada[este] = float(cada[este].replace('$', '').replace('%', ''))
    cantidades = list(range(1, int(datos['demanda']) + 1))
    lista_info = []
    for q in cantidades: 
        total = None
        for cada in tabla: 
            pedazos = [lectura(pedazo) for pedazo in cada[nombres[0]].split('-')]
            print(pedazos)
            if pedazos[0] <= q <= pedazos[1]: 
                descuento = cada[nombres[1]] / 100
                precioDesc = float(datos['producto']) * (1 - descuento)
                total = (q * precioDesc + q * cada[nombres[2]] + cada[nombres[3]])
                break
        if total is not None: 
            lista_info.append({'unidad': q, 'total': total})
    matplotlib.use('AGG')
    sns.set_theme()
    info = DataFrame(lista_info)
    sns.lmplot(data=info, y='total', x='unidad', palette=sns.color_palette("colorblind"))
    plt.title('Modelo de descuentos')
    titulo = f'descuento_{time.time_ns() * 1000}'
    plt.savefig(titulo)
    plt.close()
    legible = ''
    with open(f'{titulo}.png', 'rb') as imagen: 
        pedazos = base64.b64encode(imagen.read())
        legible = pedazos.decode()
    os.remove(f'{titulo}.png')
    legible = 'data:image/png;base64,' + legible
    pprint(cantidades)
    pprint(lista_info)
    pprint(tabla)
    return {'info': lista_info, 'imagen': legible}

def descontar_unido(titulo : str, datos : dict, verdadero = False): 
    tabla = []
    nombres = []
    with open(titulo, newline='') as nuevo: 
        info = csv.DictReader(nuevo)
        nombres = info.fieldnames
        tabla = [cada for cada in info]
    if not verdadero: os.remove(titulo)
    print(nombres)
    pprint(tabla)
    return descontar(tabla, nombres, datos)

def descontar_separado(descuentos : list[str], casillas : list[list[str]], datos : dict):
    tabla = []
    for i in range(len(casillas[0])): 
        fila = {}
        for j in range(len(descuentos)): 
            fila[descuentos[j]] = datos[casillas[j][i]]
        tabla.append(fila)
    return descontar(tabla, descuentos, datos)