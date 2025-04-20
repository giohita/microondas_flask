# Usamos una imagen base de Python con Alpine Linux, que es ligera
FROM python:3.9-alpine3.14

# Poner zona horaria a Panama para una funcion dentro del docker
RUN apk add --no-cache tzdata
ENV TZ=America/Panama
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install -r requirements.txt

# Copiamos el resto de los archivos de nuestra aplicación al contenedor
COPY . .

# Exponemos el puerto en el que correrá nuestra aplicación Flask (por defecto es 5000)
EXPOSE 5000

# Definimos el comando para ejecutar nuestra aplicación Flask
CMD ["python", "app.py"]