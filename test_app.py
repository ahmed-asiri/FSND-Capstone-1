'''
Tests for jwt flask app.
'''
import os
import json
import tempfile
import pytest

# We'll disable Auth0 calls when testing the core functionality to avoid spamming Auth0
# RBAC tests are in test_rbac.py
os.environ["DISABLE_AUTH0"] = "1"

from app import create_app
from models import Recipe, Ingredient


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
    pasta = Recipe(
        name='Pasta',
        procedure='Start by...',
        time=30)
    pasta_ingredients = [
        Ingredient(recipe_id=pasta.id,
                    name='Pasta',
                    measurement='2',
                    measurement_unit='packs'),
        Ingredient(recipe_id=pasta.id,
                    name='Tomato Paste',
                    measurement='300',
                    measurement_unit='grams'),
        Ingredient(recipe_id=pasta.id,
                    name='Onion',
                    measurement='1',
                    measurement_unit='pcs'),
    ]
    pasta.ingredients = pasta_ingredients
    pasta.insert()

    omelette = Recipe(
        name='Omelette',
        procedure='Start by...',
        time=10
    )
    omelette_ingredients = [
        Ingredient(
            recipe_id=omelette.id,
            name='Egg',
            measurement='3',
            measurement_unit='pcs'
        ),
        Ingredient(
            recipe_id=omelette.id,
            name='Pepper',
            optional=True,
            measurement='1',
            measurement_unit='pinch'
        )
    ]
    omelette.ingredients = omelette_ingredients
    omelette.insert()

def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_list_recipes(client):
    response = client.get('/recipes')
    assert response.status_code == 200
    assert len(response.json['result']) == 2


def test_get_recipe(client):
    response = client.get('/recipes/1')
    assert response.status_code == 200
    recipe = response.json['result']
    assert recipe['name'] == 'Pasta'
    assert [i['name'] for i in recipe['ingredients']] == ['Pasta', 'Tomato Paste', 'Onion']


def test_get_recipe_not_found(client):
    response = client.get('/recipes/1000')
    assert response.status_code == 404


def test_create_recipe(client):
    recipe = {
        'name': 'Pizza',
        'procedure': 'Pizza making procedure',
        'time': 30
    }
    response = client.post('/recipes', json=recipe)
    assert response.status_code == 200
  
    pizzas = Recipe.query.filter(Recipe.name == 'Pizza').count()
    assert pizzas == 1


def test_create_recipe_bad_request(client):
    '''test create recipe with missing parameters'''
    response = client.post('/recipes', json=None)
    assert response.status_code == 400


def test_update_recipe(client):
    response = client.patch('/recipes/1', json={'name': 'Burrito'})
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['result']['name'] == 'Burrito'

    response = client.get('/recipes/1')
    assert response.status_code == 200
    assert response.json['result']['name'] == 'Burrito'


def test_update_recipe_not_found(client):
    response = client.patch('/recipes/1000', json={'name': 'Burrito'})
    assert response.status_code == 404


def test_update_recipe_no_data(client):
    response = client.patch('/recipes/1', json={})
    assert response.status_code == 400


def test_delete_recipe(client):
    response = client.delete('/recipes/1')
    assert response.status_code == 200

    response = client.get('/recipes/1')
    assert response.status_code == 404


def test_delete_recipe_404(client):
    response = client.delete('/recipes/1000')
    assert response.status_code == 404


def test_get_ingredients(client):
    response = client.get('/ingredients')
    assert response.status_code == 200

    ingredients = response.json['result']
    # ingredients of test recipes
    assert len(ingredients) == 5


def test_create_ingredient(client):
    response = client.get('/recipes/1')
    recipe = response.json['result']
    recipe_ingredient_ids = [i['id'] for i in recipe['ingredients']]
    assert len(recipe_ingredient_ids) == 3

    new_ingredient = {
        'recipe_id': recipe['id'],
        'name': 'Garlic',
        'measurement': 2,
        'measurement_unit': 'cloves',
        'optional': True
    }
    response = client.post('/ingredients', json=new_ingredient)
    assert response.status_code == 200

    # get updated result
    response = client.get('/recipes/1')
    updated_recipe = response.json['result']
    assert len(updated_recipe['ingredients']) == 4
    newly_added = updated_recipe['ingredients'][-1]
    assert newly_added['name'] == 'Garlic'
    assert newly_added['measurement'] == 2
    assert newly_added['measurement_unit'] == 'cloves'
    assert newly_added['optional'] == True


def test_create_ingredient_bad_request(client):
    response = client.post('/ingredients', json=None)
    assert response.status_code == 400


def test_get_ingredient(client):
    response = client.get('/ingredients/1')
    assert response.status_code == 200
    assert response.json['result']['name'] == 'Pasta'


def test_get_ingredient_404(client):
    response = client.get('/ingredients/1000')
    assert response.status_code == 404


def test_update_ingredient(client):
    response = client.get('/ingredients/1')
    old_data = response.json
    new_data = {
        'name': 'Green Eggs',
        'measurement': 10,
        'measurement_unit': 'boxes',
        'optional': False
    }
    response = client.patch('/ingredients/1', json=new_data)
    assert response.status_code == 200
    assert response.json['result']['name'] == 'Green Eggs'
    assert response.json['result']['measurement'] == 10
    assert response.json['result']['measurement_unit'] == 'boxes'
    assert response.json['result']['optional'] == False
    assert response.json['result']['recipe_id'] == old_data['result']['recipe_id']


def test_update_ingredient_bad_request(client):
    response = client.patch('/ingredients/1', json={'random_field': 'random_value'})
    assert response.status_code == 400


def test_update_ingredient_404(client):
    response = client.patch('/ingredients/1000', json={'name': 'test'})
    assert response.status_code == 404


def test_delete_ingredient(client):
    response = client.delete('/ingredients/1')
    assert response.status_code == 200

    response = client.get('/ingredients/1')
    assert response.status_code == 404


def test_delete_ingredient_404(client):
    response = client.delete('/ingredients/1000')
    assert response.status_code == 404
