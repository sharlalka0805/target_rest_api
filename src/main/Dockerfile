FROM tensorflow/tensorflow
FROM pytorch/pytorch

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py /app/main.py

CMD ["python3", "/app/main.py"]