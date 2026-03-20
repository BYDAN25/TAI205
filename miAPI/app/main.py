#1.importaciones

from fastapi import FastAPI
from app.routers import usuarios,varios 

app=FastAPI(
    title='Mi primer API', 
    description="Mendoza Rojas Daniel",
    version='1.0.0'
)

app.include_router(usuarios.routerU)
app.include_router(varios.routerV)



