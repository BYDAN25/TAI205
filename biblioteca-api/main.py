from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

# almacenamiento simple en la memoria
libros = []
prestamos = []

# modelo del usuario
class Usuario(BaseModel):
    nombre: str
    correo: EmailStr

# modelo del libro
class Libro(BaseModel):
    nombre: str
    autor: str
    año: int
    paginas: int
    estado: str = "disponible"

# modelo del prestamo
class Prestamo(BaseModel):
    libro_nombre: str
    usuario: Usuario


# registrar los libros
@app.post("/libros", status_code=201)
def registrar_libro(libro: Libro):
    libros.append(libro.dict())
    return libro


# lista de los libros
@app.get("/libros")
def listar_libros():
    return libros


# buscar un libro
@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):
    for libro in libros:
        if libro["nombre"] == nombre:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


# registrar un prestamo
@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):

    for libro in libros:
        if libro["nombre"] == prestamo.libro_nombre:

            if libro["estado"] == "prestado":
                raise HTTPException(status_code=409, detail="Libro ya prestado")

            libro["estado"] = "prestado"
            prestamos.append(prestamo.dict())
            return {"mensaje": "Prestamo registrado"}

    raise HTTPException(status_code=404, detail="Libro no encontrado")


# devolver un libro
@app.put("/prestamos/devolver/{nombre}")
def devolver_libro(nombre: str):

    for libro in libros:
        if libro["nombre"] == nombre:
            libro["estado"] = "disponible"
            return {"mensaje": "Libro devuelto"}

    raise HTTPException(status_code=404, detail="Libro no encontrado")


# eliminar el prestamo
@app.delete("/prestamos/{nombre}")
def eliminar_prestamo(nombre: str):

    for prestamo in prestamos:
        if prestamo["libro_nombre"] == nombre:
            prestamos.remove(prestamo)
            return {"mensaje": "Prestamo eliminado"}

    raise HTTPException(status_code=409, detail="Prestamo no existe")




# Ejemplo de libro a registrar
# {
#   "nombre": "Padre Rico Padre Pobre",
#   "autor": "Robert Kiyosaki",
#   "año": 1997,
#   "paginas": 336
# }