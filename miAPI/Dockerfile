#importamos la imagen base de python 
FROM python:3.12-slim

#crear carpeta de trabajo
WORKDIR /app

#copiar requerimientos 
COPY requirements.txt .

#instalar requerimientos 
RUN pip install --no-cache-dir -r requirements.txt

#copiar archivo del API
COPY ./app ./app

#exponer puerto 
EXPOSE 5000

#Comando para ejecutar  FASRAPI
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","5000","--reload"]