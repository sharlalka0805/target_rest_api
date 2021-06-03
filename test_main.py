import pytest
from main import create_app
from dbHelperTest import dbHelperTest



# create questionAnswerTest.db DB connection
@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True

    # create the database and load questionAnswerTest.db data
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """A questionAnswerTest.db client for the app."""
    return app.test_client()


# Test Case for app route @app.route('/')
def test_Welcome(client):
    response = client.get("/")
    print(response)
    assert 200 == response.status_code


# Test Case for app route @app.route('/models', =['GET', 'PUT','DELETE'])
def test_getModels_GET(client):
    response = client.get('/models')
    assert response is not None


def test_getModels_PUT(client):
    modelData = {"name": "bert-tiny",
                 "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
                 "model": "mrm8488/bert-tiny-5-finetuned-squadv2"}
    reponse = client.put('/models', data=modelData)
    assert reponse is not None


def test_getModels_DELETE(client):
    modelName = "saSS"
    response = client.delete('/models?model=' + modelName)
    assert response is not None

    # Test Case for app route @app.route('/answer', methods=['POST'])
    # Test case for @app.route('/answer', methods=['GET'])
    # Test case for


if __name__ == '__main__':
    dbHelperTest = dbHelperTest()
    message = dbHelperTest.createDatabase()
