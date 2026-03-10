#1.imprtaciones
from fastapi import FastAPI
from typing import Optional
import asyncio

#2.Inicializacion APP
app= FastAPI(
    title='Mi Primer Api',
    description='Daniel Mendoza',
    version='1.0.0'
    ) #Funcion

#Base de datos ficticia
usuarios=[
    {"id":"1","nombre":"Daniel", "edad":"20"},
    {"id":"1","nombre":"Osiel", "edad":"22"},
    {"id":"1","nombre":"Diego", "edad":"20"},
]

#3.Endpoints
@app.get("/", tags=['Inicio'])#Endpoint de Arranque o inicio
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"} #LLave derecho json y la parte derecha valor de la llave

@app.get("/v1/bienvenidos", tags=['Inicio'])#Endpoint de Arranque o inicio
async def bien():
    return {"mensaje":"Bienvenidos"} #LLave derecho json y la parte derecha valor de la llave

@app.get("/v1/promedio/", tags=['Calificaciones'])#Endpoint de Arranque o inicio
async def promedio():
    await asyncio.sleep(3) #Peticion a otra api, consulta a la base de datos etc
    return {
        "Calificacion":"7",
        "estatus":"200"
        }

@app.get("/v1/usuario/{id}", tags=['Parametros'])#Endpoint de Arranque o inicio
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resultado":"Usuario encontrado",
        "estatus":"200"
        }
    
@app.get('/v1/usuarios_op/', tags=['Parametro Opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado": id, "Datos": usuario }
        return { "Mensaje": "usuario no encontrado" }
    else:
        return { "Aviso": "No se proporciono Id" }
