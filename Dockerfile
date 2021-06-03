FROM python:3.6.3-alpine3.6
FROM tensorflow/tensorflow
FROM pytorch/pytorch

# Creating Application Source Code Directory
RUN mkdir -p /usr/src/app

# Setting Home Directory for containers
WORKDIR /usr/src/app


# Installing python dependencies
COPY requirements.txt .
RUN pip install  -r requirements.txt

# Copying src code to Container
COPY  . /usr/src/app
RUN chmod 777 -R *

# Running Python Application
CMD ["python3", "/usr/src/app/main.py"]
