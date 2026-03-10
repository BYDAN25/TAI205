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

# Base de datos simulada
usuarios_hospedaje = [
    {"id": 1, "nombre": "Daniel", "fecha_entrada": "2026-03-09", "fecha_salida": "2026-03-12", "habitacion": "sencilla"},
    {"id": 2, "nombre": "Osiel", "fecha_entrada": "2026-03-08", "fecha_salida": "2026-03-12", "habitacion": "doble"},
    {"id": 3, "nombre": "Ivan", "fecha_entrada": "2026-03-07", "fecha_salida": "2026-03-11", "habitacion": "suite"},
    {"id": 4, "nombre": "Diego", "fecha_entrada": "2026-03-06", "fecha_salida": "2026-03-11", "habitacion": "sencilla"},
    {"id": 5, "nombre": "Mari", "fecha_entrada": "2026-03-05", "fecha_salida": "2026-03-10", "habitacion": "suite"}
]

# Modelo
class Reserva(BaseModel):
    id: int
    nombre: str = Field(min_length=3, max_length=50)
    fecha_entrada: str
    fecha_salida: str
    habitacion: str


# Seguridad HTTP Basic
seguridad = HTTPBasic()

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
    return {"mensaje": "Hola mundo FASTAPI"}


@app.get("/v1/bienvenido", tags=['Inicio'])
async def bien():
    return {"mensaje": "Bienvenido a Reservas Hospedaje"}


# Crear reserva
@app.post("/v1/reservas", tags=["CRUD Reservas"], status_code=status.HTTP_201_CREATED)
async def crear_reserva(reserva: Reserva):

    for usr in usuarios_hospedaje:
        if usr["id"] == reserva.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios_hospedaje.append(reserva.dict())

    return {
        "mensaje": "Reserva agregada correctamente",
        "reserva": reserva
    }


# Listar reservas
@app.get("/v2/reservas", tags=['CRUD Reservas'])
async def listar_reservas():
    return {
        "status": "200",
        "total": len(usuarios_hospedaje),
        "data": usuarios_hospedaje
    }


# Consultar reserva por ID
@app.get("/v3/reservas/{id}", tags=['Consultar por Id'])
async def consultar_reserva(id: int):

    for usuario in usuarios_hospedaje:
        if usuario["id"] == id:
            return {
                "Resultado": "Reserva encontrada",
                "Estatus": "200",
                "reserva": usuario
            }

    raise HTTPException(
        status_code=404,
        detail="Reserva no encontrada"
    )


# Confirmar reserva (check-in)
@app.put("/v4/reservas/{id}", tags=['Confirmar reserva'])
async def confirmar_reserva(id: int):

    for reserva in usuarios_hospedaje:
        if reserva["id"] == id:
            reserva["estado"] = "confirmada"

            return {
                "mensaje": "Reserva confirmada",
                "reserva": reserva
            }

    raise HTTPException(
        status_code=404,
        detail="Reserva no encontrada"
    )


# Cancelar reserva
@app.delete("/v5/reservas/{id}", tags=['Cancelar reserva'])
async def cancelar_reserva(id: int, userAuth: str = Depends(verificar_peticion)):

    for index, usr in enumerate(usuarios_hospedaje):
        if usr["id"] == id:
            usuarios_hospedaje.pop(index)

            return {
                "mensaje": f"Reserva cancelada por {userAuth}"
            }

    raise HTTPException(
        status_code=404,
        detail="Reserva no encontrada"
    )                                                                                