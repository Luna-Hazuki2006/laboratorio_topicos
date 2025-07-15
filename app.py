from fastapi import FastAPI, Form, status, HTTPException, File, UploadFile
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from pydantic import BaseModel
from pprint import pprint
import time
import csv
from metodos.abc import abecedear_separado, abecedear_unido
from metodos.probabilistico import probabilicear
from metodos.lote import lotear
from metodos.descuento import descontar_separado, descontar_unido
from metodos.colas import colear, colear_probabilidad
from modelos import (
    datos_form_abc, 
    dato_form_probabilistico, 
    DESCUENTOS, dato_form_cola, 
    datos_form_economico
)

app = FastAPI()
app.mount('/static', StaticFiles(directory='./static'), name='static')
templates = Jinja2Templates(directory='./templates')

@app.exception_handler(HTTPException)
async def http_exception_handler(request : Request, excepcion : HTTPException): 
    print(request.url)
    return templates.TemplateResponse(request, 'error.html', context={
        'info': excepcion.detail, 'original': request.url
    })

@app.get('/')
def iniciar(request : Request): 
    info_abc = []
    nombres_abc = []
    with open('productos.csv', 'r') as archivo: 
        contenido_abc = csv.DictReader(archivo)
        info_abc = [dato for dato in contenido_abc]
        nombres_abc = contenido_abc.fieldnames
    abc = abecedear_unido('productos.csv', True)
    info_descuento = []
    nombres_descuento = []
    with open('rangos.csv', 'r') as archivo: 
        contenido_descuento = csv.DictReader(archivo)
        info_descuento = [dato for dato in contenido_descuento]
        nombres_descuento = contenido_descuento.fieldnames
    descuento = descontar_unido('rangos.csv', {'demanda': 40, 'producto': 55}, True)
    info_colas = colear(3, 4)
    probabilidad_colas = colear_probabilidad(3, 4, 5, 1, 3)
    datos_probabilidades = dato_form_probabilistico(pedido=100, almacenamiento=0.04, acumulado=200, 
                                                    promedio=20, laborales=7, desviacion=20, perdida=0)
    probabilidades = probabilicear(datos_probabilidades)
    colas = {
        'info': info_colas, 
        'probabilidad': probabilidad_colas, 
        'anterior': {
            'llegada': 3, 
            'servicio': 4, 
            'clientes': 5, 
            'espera': 1, 
            'mayores': 3
        }
    }
    return templates.TemplateResponse(request, 'inicio.html', {
        'info_abc': info_abc, 'nombres_abc': nombres_abc, 
        'abc': abc, 'info_descuento': info_descuento, 
        'nombres_descuento': nombres_descuento, 'descuento': descuento, 
        'colas': colas, 'probabilidades': probabilidades
    })

@app.get('/abc')
def mostrar_abc(request : Request): 
    return templates.TemplateResponse(request, 'clasificacion.html')

@app.post('/abc')
def obtener_abc(request: Request, visiones : datos_form_abc, response : Response):
    print(visiones.visiones)
    resultados = ''
    if visiones.visiones == 'primero': 
        titulo = f'abc_{time.time_ns() * 1000}.csv'
        # print(visiones.archivo)
        with open(titulo, 'w') as nuevo:
            nuevo.write(visiones.archivo)
        try: 
            # return templates.TemplateResponse(request, 'respuesta_clas.html',context={
            #     'datos': abecedear_unido(titulo) 
            # })
            resultados = abecedear_unido(titulo)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Los datos de la segunda y primera columna en el archivo .csv tienen que ser números'
            )
    elif visiones.visiones == 'segundo': 
        print(visiones.visiones)
        nombres = visiones.nombres.split('\n')
        demandas = visiones.demandas.split('\n')
        costos = visiones.costos.split('\n')
        verdadd = all([x.replace('.', '').isnumeric() for x in demandas])
        verdadc = all([x.replace('.', '').isnumeric() for x in costos])
        if not verdadd or not verdadc: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Los campos tienen que contener números'
            )
        if ((len(nombres) != len(demandas) or len(nombres) != len(costos)) and 
            (visiones.nombres != '')): 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='La cantidad de productos tiene que coincidir con sus datos'
            )
        print(nombres)
        resultados = abecedear_separado(nombres, costos, demandas)
    return resultados

@app.get('/abc_res')
def dar_abc(request : Request): 
    return templates.TemplateResponse(request, 'respuesta_clas.html')

@app.get('/descuento')
def mostrar_descuentos(request : Request): 
    return templates.TemplateResponse(request, 'descuento.html')

@app.post('/descuento')
async def obtener_descuentos(datos : Request, archivo : Annotated[UploadFile, File()]):
    print(datos.client.host)
    resultados = []
    todo = await datos.form()
    if todo['visiones'] == 'primero': 
        info = await archivo.read()
        pprint(info)
        titulo = f'descuento_{time.time_ns() * 1000}.csv'
        with open(titulo, 'wb') as nuevo:
            nuevo.write(info)
        await archivo.close()
        resultados = descontar_unido(titulo, dict(todo.items()))
    elif todo['visiones'] == 'segundo': 
        partes = []
        lista = todo.keys()
        for cada in DESCUENTOS: 
            partes.append(list(filter(lambda x: cada in x, lista)))
        if partes[0] == []: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Tiene que tener al menos una fila de información'
            )
        resultados = descontar_separado(DESCUENTOS, partes, dict(todo.items()))
    
    return templates.TemplateResponse(datos, 'respuesta_descuentos.html', context={
        'resultado': resultados
    })

@app.get('/descuento_res')
def dar_descuentos(request : Request): 
    return templates.TemplateResponse(request, 'respuesta_descuentos.html')

@app.get('/pedidos')
def mostrar_pedidos(request : Request): 
    return templates.TemplateResponse(request, 'pedidos.html')

@app.post('/pedidos')
async def dar_pedidos(request : Request, Todo : Annotated[str, Form()], noseeeee: Annotated[str, Form()], datos : Annotated[UploadFile, File()]): 
    info = await request.form()
    aaaaa = await datos.read()
    async with request.form() as respuestassss:
        pprint(respuestassss)
    return {'Todo': Todo, 'nose': noseeeee, 'datos': datos, 'a': aaaaa, 'info': info.multi_items()}

@app.get('/pedidos_res')
def obtener_pedidos(request : Request): 
    return templates.TemplateResponse(request, 'respuesta_pedidos.html')

@app.get('/probabilidades')
def mostrar_probabilistico(request : Request): 
    return templates.TemplateResponse(request, 'probabilistico.html')

@app.post('/probabilidades')
def dar_probabilisticos(request : Request, datos : Annotated[dato_form_probabilistico, Form()], response : Response): 
    probabilidades = probabilicear(datos)
    return templates.TemplateResponse(request, 'respuesta_probabilistico.html', {'datos': probabilidades})

@app.get('/lote')
def mostrar_lote(request : Request): 
    return templates.TemplateResponse(request, 'economico.html')

@app.post('/lote')
def obtener_lote(request : Request, response : Request, datos : Annotated[datos_form_economico, Form()]): 
    pprint(datos)
    pprint(request)
    respuetas = lotear(datos.unitario, datos.demanda, datos.pedido, datos.almacenamiento, datos.entrega)
    return templates.TemplateResponse(request, 'respuesta_economico.html', {
        'cuerpo': respuetas
    })

@app.get('/colas')
def mostrar_cola(request : Request): 
    return templates.TemplateResponse(request, 'colas.html')

@app.post('/colas')
def obtener_cola(request : Request, datos : Annotated[dato_form_cola, Form()]): 
    if datos.llegada <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='La tasa de llegada no puede ser igual o menor a 0'
        ) 
    if datos.servicio <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='La tasa de servicio no puede ser igual o menor a 0'
        ) 
    if datos.llegada >= datos.servicio: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='La tasa de llegada no puede ser mayor a la tasa de servicios'
        )
    info = colear(datos.llegada, datos.servicio)
    probabilidad = colear_probabilidad(
        datos.llegada, datos.servicio, 
        datos.clientes, datos.espera, datos.mayores
    )
    todo = {
        'info': info, 
        'probabilidad': probabilidad, 
        'anterior': datos.model_dump()
    }
    pprint(todo)
    return templates.TemplateResponse(request, 'respuesta_colas.html', context=todo)