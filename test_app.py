'''
Tests for jwt flask app.
'''
import os
import json
import tempfile
import pytest

from app import create_app
from models import Recipe


@pytest.fixture
def client():
    db_fd, db_temp_filepath = tempfile.mkstemp()
    app = create_app({'DATABASE_URL': f'sqlite:///{db_temp_filepath}', 'TESTING': True})

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_temp_filepath)


@pytest.fixture(autouse=True)
def test_data(client):
    Recipe(
        name='Pasta',
        procedure='Start by...',
        time=30
    ).insert()


def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_list_recipes(client):
    response = client.get('/recipes')
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_recipe(client):
    response = client.get('/recipes/1')
    assert response.status_code == 200
    assert response.json['result']['name'] == 'Pasta'


def test_create_recipe(client):
    recipe = {
        'name': 'Pizza',
        'procedure': 'Pizza making procedure',
        'time': 10
    }
    response = client.post('/recipes', json=recipe)
    assert response.status_code == 200
  
    pizzas = Recipe.query.filter(Recipe.name == 'Pizza').count()
    assert pizzas == 1

def test_create_recipe_bad_request(client):
    '''test create recipe with missing parameters'''
    response = client.post('/recipes', json=None)
    assert response.status_code == 400


# def test_auth(client):
#     body = {'email': EMAIL,
#             'password': PASSWORD}
#     response = client.post('/auth', 
#                            data=json.dumps(body),
#                            content_type='application/json')

#     assert response.status_code == 200
#     token = response.json['token']
#     assert token is not None
