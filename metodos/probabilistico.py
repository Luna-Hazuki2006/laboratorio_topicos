from modelos import dato_form_probabilistico
import math
from scipy.stats import norm

def probabilicear(datos : dato_form_probabilistico): 
    e = datos.laborales * datos.promedio
    q = math.sqrt((2 * datos.pedido * e) / datos.almacenamiento)
    r = (datos.almacenamiento * q) / (datos.acumulado * e)
    r_lista = []
    respuesta = 0
    if datos.perdida != 0: 
        alter = (datos.almacenamiento * q) / (datos.almacenamiento * q + datos.perdida * e)
        r_lista = [abs(norm.ppf(dato) * datos.desviacion) + datos.promedio for dato in [r, alter]]
    else: 
        respuesta = abs(norm.ppf(r) * datos.desviacion) + datos.promedio
    return {
        'q': q, 'e': e, 'r': r, 'respuesta': respuesta, 'r_lista': r_lista
    }