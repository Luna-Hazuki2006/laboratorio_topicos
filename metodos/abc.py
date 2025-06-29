from pprint import pprint
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from pandas import DataFrame
import base64
import time
import csv
import os

def abecedear(archivo : list[dict], nombres : list[str]): 
    for cada in archivo: 
        cada[nombres[1]] = float(cada[nombres[1]])
        cada[nombres[2]] = float(cada[nombres[2]])
        cada['COSTO_TOTAL'] = cada[nombres[1]] * cada[nombres[2]]
    archivo.sort(key=lambda x: x['COSTO_TOTAL'], reverse=True)
    total = sum([cada['COSTO_TOTAL'] for cada in archivo])
    for i, cada in enumerate(archivo): 
        cada['PORCENTAJES'] = (cada['COSTO_TOTAL'] / total) * 100
        acumulado = sum([este['PORCENTAJES'] for este in archivo[:i + 1]])
        cada['CLASIFICACION'] = 'B'
        if acumulado <= 80: cada['CLASIFICACION'] = 'A'
    archivo.sort(key=lambda x: x['COSTO_TOTAL'])
    for i, cada in enumerate(archivo): 
        acumulado = sum([este['PORCENTAJES'] for este in archivo[:i + 1]])
        if acumulado <= 5: cada['CLASIFICACION'] = 'C'
    archivo.sort(key=lambda x: x['COSTO_TOTAL'], reverse=True)
    pprint(archivo)
    datos = DataFrame(archivo)
    print(datos)
    matplotlib.use('AGG')
    sns.set_theme()
    listas = Counter(datos['CLASIFICACION'])
    encontrados = datos['CLASIFICACION'].value_counts()
    pprint(listas)
    pprint(encontrados)
    sns.barplot(listas, palette=sns.color_palette("colorblind"))
    plt.title('Clasificación ABC')
    titulo = f'ABC_{time.time_ns() * 1000}'
    plt.savefig(titulo)
    plt.close()
    legible = ''
    with open(f'{titulo}.png', 'rb') as imagen: 
        pedazos = base64.b64encode(imagen.read())
        legible = pedazos.decode()
    os.remove(f'{titulo}.png')
    legible = 'data:image/png;base64,' + legible
    return {'archivo': archivo, 'imagen': legible}

def abecedear_unido(nombre : str, verdadero = False): 
    archivo = []
    nombres = []
    with open(nombre, newline='') as nuevo: 
        datos = csv.DictReader(nuevo)
        nombres = datos.fieldnames
        archivo = [cada for cada in datos]
    if not verdadero: os.remove(nombre)
    print(nombres)
    return abecedear(archivo, nombres)

def abecedear_separado(nombres : list[str], costos : list[float], demandas : list[float]): 
    pprint(nombres)
    print(costos)
    print(demandas)
    listas = []
    datos = ['Productos', 'Costos', 'Demandas']
    if len(nombres) == 0 or nombres[0] == '':
        listas = [{datos[0]: i, datos[1]: info[0], datos[2]: info[1]} for i, info in enumerate(zip(costos, demandas))]
    else: 
        listas = [{datos[0]: nom, datos[1]: costo, datos[2]: demanda} for nom, costo, demanda in zip(nombres, costos, demandas)]
    return abecedear(listas, datos)