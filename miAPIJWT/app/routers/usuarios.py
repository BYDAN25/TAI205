from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import get_current_user

routerU = APIRouter(
    prefix="/v1/usuario",
    tags=['CRUD HTTP']
)

# ------------------ GET ------------------
@routerU.get("/")
async def consulta():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

# ------------------ POST ------------------
@routerU.post("/", status_code=status.HTTP_201_CREATED)
async def crea_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    
    usuarios.append(usuario)
    
    return {
        "mensaje": "Usuario agregado correctamente",
        "usuario": usuario
    }

# ------------------ PATCH (PROTEGIDO) ------------------
@routerU.patch("/{id}")
async def actualizar_usuario(
    id: int,
    usuario_actualizado: dict,
    user: dict = Depends(get_current_user)  # 🔐 JWT
):
    for i, usuario in enumerate(usuarios):
        if usuario["id"] == id:

            usuarios[i]["nombre"] = usuario_actualizado.get("nombre", usuario["nombre"])
            usuarios[i]["edad"] = usuario_actualizado.get("edad", usuario["edad"])

            return {
                "mensaje": f"Usuario actualizado por {user['username']}",
                "status": "200",
                "usuario": usuarios[i]
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# ------------------ DELETE (PROTEGIDO) ------------------
@routerU.delete("/{id}")
async def eliminar_usuario(
    id: int,
    user: dict = Depends(get_current_user)  # 🔐 JWT
):
    for i, usuario in enumerate(usuarios):
        if usuario["id"] == id:

            usuario_eliminado = usuarios.pop(i)

            return {
                "mensaje": f"Usuario eliminado por {user['username']}",
                "status": "200",
                "usuario": usuario_eliminado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )