from pydantic import BaseModel, Field
#Modelo de validación pydantic   ---creamos el modelo
class crear_usuario(BaseModel):
    id: int = Field (...,gt=0, description="Identificador de usuario")
    nombre: str= Field(..., min_length=3, max_length=50, example="daniel")
    edad: int= Field(...,ge=1, le=123, description="Edad valida de 1 y 123")