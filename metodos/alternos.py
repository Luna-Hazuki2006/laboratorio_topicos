import os
import csv
import math
from pprint import pprint

def alternar(almacenamiento : float, entrega : float, pedido : float, titulo : str, verdadero = False):
    info = []
    nombres = []
    with open(titulo, 'r') as archivo: 
        contenido = csv.DictReader(archivo)
        info = [dato for dato in contenido]
        nombres = contenido.fieldnames
    if not verdadero: os.remove(titulo)
    pprint(info)
    pprint(nombres)
    demandaAnual5 = sum([float(mes['4']) for mes in info])
    demandaAnual4 = sum([float(mes['3']) for mes in info])
    promedioDemanda = (demandaAnual4 + demandaAnual5) / 2
    #Gerente
    menor = 1.10
    demandaTrimestral = [
        sum([float(cada['4']) for cada in info[0:3]]) * menor, 
        sum([float(cada['4']) for cada in info[3:6]]) * menor, 
        sum([float(cada['4']) for cada in info[6:9]]) * menor,
        sum([float(cada['4']) for cada in info[9:12]]) * menor,  
    ]
    #
    politicaGerente = [
        ("Demanda Anual (5° año)", round(demandaAnual5, 2)),
        ("1° Trimestre", round(demandaTrimestral[0], 2)),
        ("2° Trimestre", round(demandaTrimestral[1], 2)),
        ("3° Trimestre", round(demandaTrimestral[2], 2)),
        ("4° Trimestre", round(demandaTrimestral[3], 2))
    ]
    #Empleado
    print(promedioDemanda)
    Q = math.sqrt((2 * pedido * promedioDemanda) / almacenamiento)
    T = Q / promedioDemanda
    R = -1
    m = 0
    if T < entrega:
        R = round(promedioDemanda * entrega, 2)
    else:
        while R == -1:
            if (entrega - m * T) > 0 and (entrega - (m + 1) * T) < 0: R = round(promedioDemanda * (entrega - m * T), 2)
            else: m += 1
    #
    politicaEmpleado = [
        ("Demanda Anual (Promedio entre años 4 y 5)", round(promedioDemanda, 2)),
        ("Cantidad de Pedido (Q)", round(Q, 2)),
        ("Tiempo entre pedidos (T)", round(T, 2)),
        ("Punto de Reorden (R)", R)
    ]
    return {
        'info': info, 
        'empleados': politicaEmpleado, 
        'gerentes': politicaGerente
    }