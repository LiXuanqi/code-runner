import pytest

from coderunner import create_app


@pytest.fixture()
def app():
    app = create_app({
        'TESTING': True
    })

    yield app


@pytest.fixture()
def client(app):
    """A test client for the app"""
    return app.test_client()


def test_hello(client):
    rv = client.get('/hello')
    assert b'Hello, World!' in rv.data


def test_run_python(client):
    rv = client.post('/run', json={
        'language': 'python',
        'code': 'print("Hello")'
    })
    json_data = rv.get_json()
    assert json_data['result'] == "Hello\n"
