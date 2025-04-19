# Usamos una imagen base de Python con Alpine Linux, que es ligera
FROM python:3.9-alpine3.14

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install -r requirements.txt

# Copiamos el resto de los archivos de nuestr aplicación al contenedor
COPY . .

# Exponemos el puerto en el que correrá nuestra aplicación Flask (por defecto es 5000)
EXPOSE 5000

# Definimos el comando para ejecutar nuestra aplicación Flask
CMD ["python", "app.py"]