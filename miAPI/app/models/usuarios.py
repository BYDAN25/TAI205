from pydantic import BaseModel, Field
#Modelo de validación pydantic   ---creamos el modelo
class crear_usuario(BaseModel):
    nombre: str= Field(..., min_length=3, max_length=50, example="Daniel")
    edad: int= Field(...,ge=1, le=123, description="Edad valida de 1 y 123")