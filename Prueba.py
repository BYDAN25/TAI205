# IMPORTACIONES
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
import asyncio
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# INICIALIZACION DE LA API
app = FastAPI(
    title="API de Ejemplo - Estudio Examen",
    description="Daniel Mendoza",
    version="1.0.0"
)

# BASE DE DATOS SIMULADA
usuarios = [
    {"id": 1, "nombre": "Daniel", "edad": 20},
    {"id": 2, "nombre": "Osiel", "edad": 22},
]

libros = []
prestamos = []

# MODELOS PYDANTIC

class Usuario(BaseModel):
    id: int = Field(
        ...,
        gt=0,
        description="Identificador único",
        json_schema_extra={"example": 1}
    )

    nombre: str = Field(
        ...,
        min_length=3,
        max_length=50,
        json_schema_extra={"example": "Daniel"}
    )

    edad: int = Field(
        ...,
        ge=1,
        le=120,
        json_schema_extra={"example": 20}
    )


class UsuarioRegistro(BaseModel):
    nombre: str
    correo: EmailStr


class Libro(BaseModel):
    nombre: str
    autor: str
    año: int
    paginas: int
    estado: str = "disponible"


class Prestamo(BaseModel):
    libro_nombre: str
    usuario: UsuarioRegistro


# SEGURIDAD HTTP BASIC

seguridad = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):

    userAuth = secrets.compare_digest(credenciales.username, "daniel")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )

    return credenciales.username


# ENDPOINTS BASICOS

@app.get("/", tags=["Inicio"])
async def hola_mundo():
    return {"mensaje": "Hola mundo FASTAPI"}


@app.get("/bienvenidos", tags=["Inicio"])
async def bienvenidos():
    return {"mensaje": "Bienvenidos a la API"}


@app.get("/promedio", tags=["Ejemplo Async"])
async def promedio():

    await asyncio.sleep(2)

    return {
        "calificacion": 7.5,
        "estatus": 200
    }


# CRUD USUARIOS

@app.get("/usuarios", tags=["CRUD Usuarios"], response_model=List[Usuario])
async def obtener_usuarios():
    return usuarios


@app.get("/usuarios/{id}", tags=["CRUD Usuarios"])
async def obtener_usuario(id: int):

    for usuario in usuarios:
        if usuario["id"] == id:
            return usuario

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.get("/usuarios_opcional/", tags=["Parametros"])
async def usuario_opcional(id: Optional[int] = None):

    if id is None:
        return {"mensaje": "No se proporciono id"}

    for usuario in usuarios:
        if usuario["id"] == id:
            return usuario

    return {"mensaje": "Usuario no encontrado"}


@app.post("/usuarios", tags=["CRUD Usuarios"], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: Usuario):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado correctamente",
        "usuario": usuario
    }


@app.put("/usuarios/{id}", tags=["CRUD Usuarios"])
async def actualizar_usuario(id: int, usuario_actualizado: Usuario):

    for index, usr in enumerate(usuarios):

        if usr["id"] == id:
            usuarios[index] = usuario_actualizado.dict()

            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuario_actualizado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.delete("/usuarios/{id}", tags=["CRUD Usuarios"])
async def eliminar_usuario(
        id: int,
        userAuth: str = Depends(verificar_peticion)
):

    for index, usr in enumerate(usuarios):

        if usr["id"] == id:

            usuarios.pop(index)

            return {
                "mensaje": f"Usuario eliminado por {userAuth}"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# CRUD LIBROS

@app.post("/libros", tags=["Libros"], status_code=201)
def registrar_libro(libro: Libro):

    libros.append(libro.dict())

    return libro


@app.get("/libros", tags=["Libros"])
def listar_libros():
    return libros


@app.get("/libros/{nombre}", tags=["Libros"])
def buscar_libro(nombre: str):

    for libro in libros:
        if libro["nombre"] == nombre:
            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


# PRESTAMOS

@app.post("/prestamos", tags=["Prestamos"])
def registrar_prestamo(prestamo: Prestamo):

    for libro in libros:

        if libro["nombre"] == prestamo.libro_nombre:

            if libro["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="Libro ya prestado"
                )

            libro["estado"] = "prestado"

            prestamos.append(prestamo.dict())

            return {"mensaje": "Prestamo registrado"}

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.put("/prestamos/devolver/{nombre}", tags=["Prestamos"])
def devolver_libro(nombre: str):

    for libro in libros:

        if libro["nombre"] == nombre:

            libro["estado"] = "disponible"

            return {"mensaje": "Libro devuelto"}

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.delete("/prestamos/{nombre}", tags=["Prestamos"])
def eliminar_prestamo(nombre: str):

    for prestamo in prestamos:

        if prestamo["libro_nombre"] == nombre:

            prestamos.remove(prestamo)

            return {"mensaje": "Prestamo eliminado"}

    raise HTTPException(
        status_code=409,
        detail="Prestamo no existe"
    )