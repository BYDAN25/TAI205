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

usuarios = [
    {"id": 1, "nombre": "osiel", "edad": "22"},
    {"id": 2, "nombre": "daniel", "edad": "43"},
    {"id": 3, "nombre": "diego", "edad": "20"}
    #{"id": 1, "paciente": "Juan", "fecha": "2026-03-15", "hora": "10:00"}
]


class Usuario(BaseModel):  #Aqui se cambia usuario por el otro
    id: str = Field(min_length=1)
    nombre: str = Field(min_length=3, max_length=50)
    edad: int = Field(gt=0, lt=100)
    #fecha: str
    #hora: str
    
    
    #o
    #   paciente: str = Field(min_length=3, max_length=50)
    #   fecha: str
    #   hora: str


# seguridad http basic
seguridad = HTTPBasic()


def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "daniel")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas"
        )
    return credenciales.username

# CRUD BASICO
# GET -> consultar datos
# POST -> agregar registro
# PUT -> actualizar registro
# DELETE -> eliminar registro

@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje": "Hola mundo FASTAPI"}


@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bien():
    return {"mensaje": "Bienvenidos"}


@app.get("/v2/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3)
    return {
        "Calificacion": "7.5",
        "estatus": "200"
    }


@app.get("/v3/usuarioss/{id}", tags=['Parametros']) #/v3/algo/{id}
async def consultaUno(id: int):
    await asyncio.sleep(3)

    for usuario in usuarios:
        if usuario["id"] == id:
            return {
                "Resultado": "usuario encontrado",
                "Estatus": "200",
                "usuario": usuario
            }

    return {"Mensaje": "Usuario no encontrado"}


@app.get("/v4/usuarios_op/", tags=['Parametro Opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(2)

    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario encontrado": id, "Datos": usuario}

        return {"Mensaje": "Usuario no encontrado"}

    else:
        return {"Aviso": "No se proporciono id"}


@app.get("/v5/usuarios/", tags=['CRUD HTTP'])   #Aqui cambiar solamente usuarios por el otro
async def consultaT():
    return {
        "status": "200",
        "total": len(usuarios),   #cambiar a len algo
        "data": usuarios
    }


@app.post("/v1/usuarios/", tags=['CRUD HTTP']) #Aqui cambiar solamente usuarios por el otro
async def crear_usuario(usuario: Usuario): #Cambiar a crear_tal cosa

    for usr in usuarios:
        if usr["id"] == int(usuario.id):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe" #Ya existe la cita o algo por el estilo
            )

    usuarios.append({
        "id": int(usuario.id),
        "nombre": usuario.nombre,
        "edad": str(usuario.edad)
        
        #citas.append({
        #"id": int(cita.id),
        #"paciente": cita.paciente,
        #"fecha": cita.fecha,
        #"hora": cita.hora
    })

    return {
        "mensaje": "usuario agregado correctamente",
        "status": "200",
        "usuario": usuario
    }


@app.put("/v1/usuarios/", tags=['CRUD HTTP']) #Aqui cambiar solamente usuarios por el otro
async def actualizar_usuario(id: int, usuario_actualizado: dict): #Actualizar_tal cosa

    for usr in usuarios: #for cita in citas:
        if usr["id"] == id:
            usuario_actualizado["id"] = id
            usr.update(usuario_actualizado)

            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"    #tal cosa no encontrada
    )


@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])  #Aqui cambiar solamente usuarios por el otro
async def elimina_usuario(id: int, userAuth: str = Depends(verificar_peticion)):

    for index, usr in enumerate(usuarios): #for index, cita in enumerate(citas):
        if usr["id"] == id:
            usuarios.pop(index)

            return {
                "mensaje": f"Usuario eliminado por {userAuth}" #Tal cosa eliminada
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"   #Tal cosa no encontrada
    )