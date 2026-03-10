from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(
    title="Practica 4 - Pydantic",
    description="API con validaciones usando Pydantic",
    version="1.0"
)

usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]

class CrearUsuario(BaseModel):
    id: int = Field(
        ...,
        gt=0,
        description="Identificador único del usuario (mayor a 0)",
        json_schema_extra={"example": 4}
    )

    nombre: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nombre del usuario (entre 3 y 50 caracteres)",
        json_schema_extra={"example": "Juanita"}
    )

    edad: int = Field(
        ...,
        ge=1,
        le=123,
        description="Edad válida entre 1 y 123 años",
        json_schema_extra={"example": 25}
    )


@app.get("/v1/usuarios/", response_model=List[CrearUsuario])
async def obtener_usuarios():
    return usuarios


@app.post("/v1/usuarios/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: CrearUsuario):

    # Validar que el ID no exista
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    # Agregar usuario a la lista
    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado correctamente",
        "usuario": usuario
    }