from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Base de datos temporal
usuarios = []

class Usuario(BaseModel):
    id: int
    nombre: str
    edad: int

# GET
@app.get("/usuarios", response_model=List[Usuario])
def obtener_usuarios():
    return usuarios

# POST
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    usuarios.append(usuario)
    return {"mensaje": "Usuario agregado"}

# PUT
@app.put("/usuarios/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario_actualizado: Usuario):
    for i, u in enumerate(usuarios):
        if u.id == usuario_id:
            usuarios[i] = usuario_actualizado
            return {"mensaje": "Usuario actualizado"}
    return {"error": "Usuario no encontrado"}

# DELETE
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    for i, u in enumerate(usuarios):
        if u.id == usuario_id:
            usuarios.pop(i)
            return {"mensaje": "Usuario eliminado"}
    return {"error": "Usuario no encontrado"}
