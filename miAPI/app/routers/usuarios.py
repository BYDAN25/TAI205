from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.models.usuarios import crear_usuario
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB
from app.security.auth import verificar_peticion

routerU = APIRouter(
    prefix="/v1/usuario",
    tags=['CRUD HTTP']
)

# 🔹 GET - SIN seguridad
@routerU.get("/")
async def consulta(db: Session = Depends(get_db)):
    usuarios = db.query(usuarioDB).all()

    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

# 🔹 POST - SIN seguridad
@routerU.post("/", status_code=status.HTTP_201_CREATED)
async def crea_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):

    usuarioNuevo = usuarioDB(
        nombre=usuarioP.nombre,
        edad=usuarioP.edad
    )

    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)

    return {
        "mensaje": "Usuario agregado correctamente",
        "usuario": usuarioNuevo
    }

# 🔹 PATCH - SIN seguridad
@routerU.patch("/{id}")
async def actualizar_usuario(id: int, usuario_actualizado: crear_usuario, db: Session = Depends(get_db)):

    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario.nombre = usuario_actualizado.nombre
    usuario.edad = usuario_actualizado.edad

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "Usuario actualizado correctamente",
        "usuario": usuario
    }

# 🔹 DELETE - CON seguridad
@routerU.delete("/{id}")
async def eliminar_usuario(
    id: int,
    db: Session = Depends(get_db),
    userAuth: str = Depends(verificar_peticion) 
):

    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {
        "mensaje": f"Usuario eliminado por {userAuth}",
        "usuario": usuario
    }