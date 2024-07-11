FROM ubuntu:latest
LABEL authors="franco"

ENTRYPOINT ["top", "-b"]

# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requerimientos y instalar las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto a /app
COPY . .

# Establecer la variable de entorno Flask
ENV FLASK_APP=run.py

# Exponer el puerto en el que la app correrá
EXPOSE 8080

# Comando para correr la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
