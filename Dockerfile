# Use an official Python runtime as a parent image
FROM frolvlad/alpine-python3:latest

# Set the working directory to /app
WORKDIR /ProyectoCC

# Copy the current directory contents into the container at /app
COPY requirements.txt /ProyectoCC/
COPY app_flask.py /ProyectoCC/
COPY 

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 80
EXPOSE 80

# Define environment variable
# ENV PORT 5000

# Run app.py when the container launches
# CMD ["python3", "app_flask.py"]
