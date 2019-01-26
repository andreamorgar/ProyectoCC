# Utilizamos la imagen elegida
FROM frolvlad/alpine-python3:latest

# Establecemos directorio de trabajo to /ProyectoCC
WORKDIR /ProyectoCC

# Instalamos los paquetes necesarios en requirements.txt
COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

# Copiamos los ficheros al container en la ruta /ProyectoCC
COPY app_flask.py predictionDB.py weather_class.py ./
#/ProyectoCC/

# Permitimos que el puerto 80 esté disponible
EXPOSE 80

# Definimos variable de entorno necesaria para que al iniciar nuestra app se
# conecte a mLab y no a una base de datos local
ENV MLAB_OR_MONGO mlab

# Establecemos que el servicio arranque cuando se lance el contenedor
CMD ["python3", "app_flask.py"]
