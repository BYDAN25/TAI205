from fastapi import FastAPI
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field
import asyncio
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


app = FastAPI(
    title='Mi primer API',
    description="Mendoza Rojas Daniel",
    version='1.0.0'
)

usuarios_hospedaje = [{
    "id": 1, "nombre": "Daniel", "Fecha_entrada": "2026-03-09", "Fecha_salida": "2026-03-12", "habitacion": "sencilla",
    "id": 2, "nombre": "Osiel", "Fecha_entrada": "2026-03-08", "Fecha_salida": "2026-03-12", "habitacion": "doble",
    "id": 3, "nombre": "Ivan", "Fecha_entrada": "2026-03-07", "Fecha_salida": "2026-03-11", "habitacion": "suite",
    "id": 4, "nombre": "Diego", "Fecha_entrada": "2026-03-06", "Fecha_salida": "2026-03-11", "habitacion": "sencilla",
    "id": 5, "nombre": "Mari", "Fecha_entrada": "2026-03-05", "Fecha_salida": "2026-03-10", "habitacion": "suite", 
}]

class reservas(BaseModel):
    id: str = Field(min_length=1)
    nombre: str = Field(min_length=5, max_length=50)
    fecha_entrada: str
    fecha_salida: str
    habitacion: int
    
seguridad = HTTPBasic

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "hotel")
    passAuth = secrets.compare_digest(credenciales.password, "r2026")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas"
        )
    return credenciales.username

@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"} #LLave derecho json y la parte derecha valor de la llave

@app.get("/bienvenido")#Endpoint de Arranque o inicio
@app.get("/v1/bienvenido", tags=['Inicio'])
async def bien():
    return {"mensaje":"Bienvenido a Reservas Hospedaje"} #LLave derecho json y la parte derecha valor de la llave

#Crear reserva
@app.post("/v1/usuarios_hospedaje", tags=["CRUD usuarios_hospedaje: Crear reserva"], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarios_hospedaje: usuarios_hospedaje):

    for usr in usuarios_hospedaje:
        if usr["id"] == usuarios_hospedaje.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios_hospedaje.append(usuarios_hospedaje.dict())

    return {
        "mensaje": "Usuario agregado correctamente",
        "usuario": usuarios_hospedaje
    }

#Listar reservas
@app.get("/v2/usuarios/", tags=['CRUD HTTP'])   #Aqui cambiar solamente usuarios por el otro
async def consultaT():
    return {
        "status": "200",
        "total": len(usuarios_hospedaje),   #cambiar a len algo
        "data": usuarios_hospedaje
    }

#Consultar por ID
@app.get("/v3/usuarios_hospedaje/{id}", tags=['Consultar por Id']) #/v3/algo/{id}
async def consultaUno(id: int):
    await asyncio.sleep(3)

    for usuario in usuarios_hospedaje:
        if usuario["id"] == id:
            return {
                "Resultado": "usuario encontrado",
                "Estatus": "200",
                "usuario": usuario
            }
            

    return {"Mensaje": "Usuario no se encontrado"}

#Este get debe de confirmar la reserva
#Confirmar la reserva osea checkin
@app.get("/v3/usuarios_hospedaje/{id}", tags=['Consultar por Id']) #/v3/algo/{id}
async def consultaUno(id: int):
    await asyncio.sleep(3)

    for usuario in usuarios_hospedaje:
        if usuario["id"] == id:
            return {
                "Resultado": "usuario encontrado",
                "Estatus": "200",
                "usuario": usuario
            }
            

    return {"Mensaje": "Usuario no se encontrado"}


#Cancelar reserva
@app.delete("/v5/usuarios_hospedaje/{id}", tags=['Cancelar reserva'])  #Aqui cambiar solamente usuarios por el otro
async def elimina_usuario(id: int, userAuth: str = Depends(verificar_peticion)):

    for index, usr in enumerate(usuarios_hospedaje): #for index, cita in enumerate(citas):
        if usr["id"] == id:
            usuarios_hospedaje.pop(index)

            return {
                "mensaje": f"Usuario eliminado por {userAuth}" #Tal cosa eliminada
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado")   #Tal cosa no encontrada
