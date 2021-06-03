FROM python:3.7.4-alpine
FROM tensorflow/tensorflow
FROM pytorch/pytorch

# Creating Application Source Code Directory
RUN mkdir -p /usr/src/app

# Setting Home Directory for containers
WORKDIR /usr/src/app

ENV PATH=/usr/lib/postgresql/X.Y/bin/:$PATH

# Installing python dependencies
COPY requirements.txt .
RUN pip install  -r requirements.txt

# Copying src code to Container
COPY  . /usr/src/app
RUN chmod 777 -R *

# Running Python Application
CMD ["python3", "/usr/src/app/main.py"]
