# Use an official Python runtime as a parent image
FROM frolvlad/alpine-python3:latest

# Set the working directory to /ProyectoCC
WORKDIR /ProyectoCC

# Install any needed packages specified in requirements.txt
COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

# Copy the files into the container at /ProyectoCC
COPY app_flask.py predictionDB.py weather_class.py /ProyectoCC/

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python3", "app_flask.py"]
