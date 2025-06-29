from modelos import dato_form_probabilistico
import math
from scipy.stats import norm

def probabilicear(datos : dato_form_probabilistico): 
    e = datos.laborales * datos.promedio
    q = math.sqrt((2 * datos.pedido * e) / datos.almacenamiento)
    r = (datos.almacenamiento * q) / (datos.acumulado * e)
    if datos.perdida: 
        alter = (datos.almacenamiento * q) / (datos.almacenamiento * q + datos.perdida * e)
        r_lista = [(norm.ppf(dato) * datos.desviacion) + datos.promedio for dato in [r, alter]]
    else: 
        respuesta = (norm.ppf(r) * datos.desviacion) + datos.promedio
    