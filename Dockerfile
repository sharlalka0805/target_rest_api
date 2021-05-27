FROM tensorflow/tensorflow
FROM pytorch/pytorch

# Creating Application Source Code Directory
RUN mkdir -p /usr/src/app

# Setting Home Directory for containers
WORKDIR /usr/src/app

# Installing python dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copying src code to Container
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN chmod 777 -R *

# Application Environment variables
#ENV PORT 8080

# Exposing Ports
#EXPOSE $PORT

# Setting Persistent data
VOLUME ["/app-data"]

# Running Python Application
CMD ["python3", "/src/main/main.py"]