import os
import tempfile
from starnavi.app import app
import pytest
import json
import names


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_register(client):
    rv = client.post('/register', json={'email': f'{names.get_first_name("male").lower()}@mail.com',
                                        'password': 'test123', 'first_name': names.get_first_name('male'),
                                        'last_name': names.get_last_name(), 'birth_date': '16-11-1997'})
    assert {'status': 200} == json.loads(rv.data.decode('utf-8'))


def test_login(client):
    rv = client.post('/login', json={'email': 'daniel@mail.com', 'password': 'test123'})
    assert 'access_token' in json.loads(rv.data.decode('utf-8'))


def test_post(client):
    rv = client.post('/newpost', json={'title': 'Prodam Garaj', 'body': 'Nedorogo', 'user_id': 1})

    assert 'status' in json.loads(rv.data.decode('utf-8'))


def test_like(client):
    rv = client.post('/like/1')

    assert 'message' in json.loads(rv.data.decode('utf-8'))


def test_unlike(client):
    rv = client.delete('/like/1')

    assert 'message' in json.loads(rv.data.decode('utf-8'))