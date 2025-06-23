from fastapi import FastAPI, Form, status, HTTPException, File
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from pydantic import BaseModel
from pprint import pprint
import time
from metodos.abc import abecedear_separado, abecedear_unido

app = FastAPI()
app.mount('/static', StaticFiles(directory='./static'), name='static')
templates = Jinja2Templates(directory='./templates')

class datos_form_abc(BaseModel): 
    visiones: str
    archivo: str
    nombres: str
    costos: str
    demandas: str

@app.get('/')
def iniciar(request : Request): 
    return templates.TemplateResponse(request, 'inicio.html')

@app.get('/abc')
def mostrar_abc(request : Request): 
    return templates.TemplateResponse(request, 'clasificacion.html')

@app.post('/abc')
def obtener_abc(request: Request, visiones : datos_form_abc, response : Response):
    print(visiones.visiones)
    if visiones.visiones == 'primero': 
        titulo = f'abc_{time.time_ns() * 1000}.csv'
        # print(visiones.archivo)
        with open(titulo, 'w') as nuevo:
            nuevo.write(visiones.archivo)
        try: 
            # return templates.TemplateResponse(request, 'respuesta_clas.html',context={
            #     'datos': abecedear_unido(titulo) 
            # })
            return abecedear_unido(titulo)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Los datos de la segunda y primera columna en el archivo .csv tienen que ser números'
            )
    elif visiones.visiones == 'segundo': 
        print(visiones.visiones)
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
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
        return abecedear_separado(nombres, costos, demandas)
    return 

@app.get('/abc_res')
def dar_abc(request : Request): 
    return templates.TemplateResponse(request, 'respuesta_clas.html')