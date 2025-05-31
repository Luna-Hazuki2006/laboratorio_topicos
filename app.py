from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory='./static'), name='static')
templates = Jinja2Templates(directory='./templates')

@app.get('/')
def mostrar(request : Request): 
    return templates.TemplateResponse(request, 'index.html')
