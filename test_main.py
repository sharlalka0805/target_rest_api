import time
from unittest.mock import patch
import pytest
from main import create_app
from transformers import pipeline
from google.cloud import storage

@pytest.fixture(scope='session')
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# test
def test_API(client):
    r = client.get("/")
    assert 200 == r.status_code


# test /answer Post
@patch('main.models', {
        "default": "distilled-bert",
        "models": [
            {
                "name": "distilled-bert",
                "tokenizer": "distilbert-base-uncased-distilled-squad",
                "model": "distilbert-base-uncased-distilled-squad",
                "pipeline": pipeline('question-answering',
                                     model="distilbert-base-uncased-distilled-squad",
                                     tokenizer="distilbert-base-uncased-distilled-squad")
            }
        ]
    })
@patch('main.environment', 'TEST')
def test_answer_POST(client):
    print("Testing post answer")
    payload = {"question": "who did holly matthews play in waterloo rd?",
               "context": "She attended the British drama school East 15 in 2005,"
                          "and left after winning a high-profile role "
                        "in the BBC drama Waterloo Road, playing the bully eigh-Ann Galloway."
                        "[6] Since that role,Matthews has continued to act in BBC's Doctors, playing Connie  "
                        " Whitfield; in ITV's The Bill playing drug addict Josie Clarke;"
                        " and she was back in the BBC soap Doctors in 2009, playing Tansy Flack."}
    r = client.post("/answer", json=payload)
    assert 200 == r.status_code


#test /answer GET
@patch('main.models', {
        "default": "distilled-bert",
        "models": [
            {
                "name": "distilled-bert",
                "tokenizer": "distilbert-base-uncased-distilled-squad",
                "model": "distilbert-base-uncased-distilled-squad",
                "pipeline": pipeline('question-answering',
                                     model="distilbert-base-uncased-distilled-squad",
                                     tokenizer="distilbert-base-uncased-distilled-squad")
            }
        ]
    })
@patch('main.environment', 'TEST')
def test_answer_GET(client):
    print("Testing Add Model functionality")
    start_Time = int(time.time())
    endTime = int(time.time())
    url = "/answer?start="+str(start_Time)+'&end='+str(endTime)
    r = client.get(url)
    assert 200 == r.status_code


# # test /models GET -- TESTED
@patch('main.models', {
        "default": "distilled-bert",
        "models": [
            {
                "name": "distilled-bert",
                "tokenizer": "distilbert-base-uncased-distilled-squad",
                "model": "distilbert-base-uncased-distilled-squad",
                "pipeline": pipeline('question-answering',
                                     model="distilbert-base-uncased-distilled-squad",
                                     tokenizer="distilbert-base-uncased-distilled-squad")
            }
        ]
    })
@patch('main.environment', 'TEST')
def test_models_GET(client):
    r = client.get("/models")
    assert 200 == r.status_code


# Test /models DELETE --- TESTED
@patch('main.models', {
        "default": "distilled-bert",
        "models": [
            {
                "name": "distilled-bert",
                "tokenizer": "distilbert-base-uncased-distilled-squad",
                "model": "distilbert-base-uncased-distilled-squad",
                "pipeline": pipeline('question-answering',
                                     model="distilbert-base-uncased-distilled-squad",
                                     tokenizer="distilbert-base-uncased-distilled-squad")
            }
        ]
    })
@patch('main.environment', 'TEST')
def test_models_DELETE(client):
    r = client.delete("/models?model=bert-tiny")
    assert 400 == r.status_code


# test /models PUT --- TESTED
@patch('main.models', {
        "default": "distilled-bert",
        "models": [
            {
                "name": "distilled-bert",
                "tokenizer": "distilbert-base-uncased-distilled-squad",
                "model": "distilbert-base-uncased-distilled-squad",
                "pipeline": pipeline('question-answering',
                                     model="distilbert-base-uncased-distilled-squad",
                                     tokenizer="distilbert-base-uncased-distilled-squad")
            }
        ]
    })
@patch('main.environment', 'TEST')
def test_models_PUT(client):
    print("Testing Add Model functionality")
    payload = {
			"name": "deepset-roberta",
			"tokenizer": "deepset/roberta-base-squad2",
			"model": "deepset/roberta-base-squad2"
		}
    r = client.put("/models", json=payload)
    assert 200 == r.status_code

