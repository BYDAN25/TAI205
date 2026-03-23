# 1. importaciones

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.routers import usuarios, varios
from app.security.auth import authenticate_user, create_access_token


app = FastAPI(
    title='Mi primer API',
    description="Mendoza Rojas Daniel",
    version='1.0.0'
)

# Routers
app.include_router(usuarios.routerU)
app.include_router(varios.routerV)


# 🔐 LOGIN JWT
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,  # 🔥 mejor que 400 (más correcto en auth)
            detail="Credenciales incorrectas"
        )

    access_token = create_access_token({
        "sub": user["username"]
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }