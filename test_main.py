import pytest
from main import create_app

import time
import sqlite3

timestamp = int(time.time())

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
def test_health(client):
    r = client.get("/")
    assert 200 == r.status_code
def test_addModel(client):
    print("Testing Add Model functionality")
    # Test add a model functionality
    payload = {
        "name": "distilled-ber",
        "tokenizer": "distilbert-base-uncased-distilled-squad",
        "model": "distilbert-base-uncased-distilled-squad"
    }
    r = client.put("/models", json=payload)
    assert 200 == r.status_code

def test_getModel(client):
    # test /models GET
    r = client.get("/models")
    assert 200 == r.status_code

def test_deleteModel(client):
    # Test /models DELETE
    r = client.delete("/models?model=bert-tiny")
    assert 200 == r.status_code