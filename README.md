# RecipeHub

API for managing your cooking recipes.

Live Heroku deployment: https://fsnd-recipehub.herokuapp.com/recipes

## Motivation

This is my capstone project submission for the Udacity Full-Stack Developer Nanodegree program.

The goal is to demonstrate the ability to:

- Design data models and their relations using SQLAlchemy.
- Write database queries using SQLAlchemy.
- Design an HTTP API with Flask.
- Document the API and development guide in detail.
- Implement authentication and Role Based Access Control using Auth0.
- Test the API and access control capabilities.
- Provide PEP8 compliant, and readable code.
- Deploy the app to Heroku.

## Authentication when using live deployment

The Heroku deployment requires authentication to start using. There are two access levels: ReadOnly and Admin.

For testing the live deployment, a Postman collection with access tokens is provided for convenience (`fsnd-recipehub.postman_collection.json`).

For automated tests, please see the **Testing** section.

For authentication details, please see the **Authentication and Permissions** section later in the document.

## Development Setup

Install dependencies:

```
pip install -r requirements.txt
```

Start the app locally:

```
source setup.sh
flask run --reload
```

## Deployment

To update your Heroku deployment with latest changes:

```
git push heroku master
```

To deploy the app to Heroku from scratch, keep reading.

### New Heroku deployment

First, you need a free Heroku account and have the heroku client installed. Please see [the official docs](https://devcenter.heroku.com/) on how to do these.

#### Create a Heroku app

```
heroku create <app_name>
```

When successful you should have a `heroku` remote in your repo with address:

```
https://git.heroku.com/<app_name>.git
```

#### Add Postgres addon

```
heroku addons:create heroku-postgresql:hobby-dev --app <app_name>
```

This will setup a database and make its connection string available as `DATABASE_URL` environment variable.

#### Set configuration variables

You can set your app's config variables from the web dashboard's app settings. 

You can also do it from the command line. For example:

```
heroku config:set AUTH0_DOMAIN="mydomain.auth0.com"
```

Check your app's current config with:

```
heroku config
```

## Testing

There is a `DISABLE_AUTH0` environment variable that's used in testing.
The main reasons to disable authentication are to avoid spamming Auth0 with our test requests, and keep the main functionality tests shorter.

The app functionality tests are in `test_app.py`. This test module uses `DISABLE_AUTH0=1` setting.

```
source setup.sh
pytest test_app.py
```

The access control tests make requests to Auth0, and should be run every so often. This test module unsets `DISABLE_AUTH0` variable.

```
source setup.sh
pytest test_rbac.py
```

### Style Guide

The source follows PEP8. Please use `pycodestyle` for guidance:

```
pycodestyle --exclude=env .
```

## Endpoints

### `GET /`

The only public endpoint, for debugging. Returns: `"Healthy"`

### `GET /recipes`

- Returns the list of recipes.
- Required headers:
  - `Authorization` header with bearer token that has `read:recipes` permission.
- Request arguments: None
- Returns:
  - `200 OK` response, body with a `result` key, its value being the list of recipes.

Example response:
```json
{
  "result": [
    {
      "id": 1,
      "name": "Pizza",
      "procedure": "Est qui alias molestias facilis et et eum. Ducimus est corrupti et qui. Et quidem nostrum qui ipsum perspiciatis et enim. Odio impedit et unde voluptatem.",
      "time": 30,
      "ingredients": [
        {
            "id": 1,
            "recipe_id": 1,
            "name": "Flour",
            "optional": false,
            "measurement": 250,
            "measurement_unit": "grams"
        }
      ],
    }
  ]
}
```

### `GET /recipes/<recipe_id>`

- Returns a single recipe.
- Required headers:
  - `Authorization` header with bearer token that has `read:recipes` permission.
- Request path arguments: `recipe_id`
- Returns:
  - `200 OK` response, body with a `result` key, value being the recipe object.
  - `404 Not Found` response when an unknown recipe ID was provided.

Example response:
```json
{
  "result": {
    "id": 1,
    "name": "Pizza",
    "procedure": "Est qui alias molestias facilis et et eum. Ducimus est corrupti et qui. Et quidem nostrum qui ipsum perspiciatis et enim. Odio impedit et unde voluptatem.",
    "time": 30,
    "ingredients": []
  }
}
```

### `POST /recipes`

- Adds a new recipe.
- Required headers:
  - `Authorization` header with bearer token that has `create:recipes` permission.
- Request body:
  - `name`: Recipe name string
  - `procedure`: Recipe instruction string
  - `ingredients`: List of `Ingredient` objects
  - `time`: Time to cook minutes, integer
- Returns:
  - `200 OK` response when a new record was successfully created.
    `400 Bad Request` response when any of the fields are missing.

Example response:
```json
{
    "success": true,
    "result": {
        "id": 1,
        "name": "Pizza",
        "procedure": "Est qui alias molestias facilis et et eum. Ducimus est corrupti et qui. Et quidem nostrum qui ipsum perspiciatis et enim. Odio impedit et unde voluptatem.",
        "time": 30,
        "ingredients": []
    }
}
```

### `PATCH /recipes/<recipe_id>`

- Updates a recipe.
- Required headers:
  - `Authorization` header with bearer token that has `update:recipes` permission.
- Request path argument: `recipe_id`
- Request body (can be a subset of):
  - `name`: Recipe name string
  - `procedure`: Recipe instruction string
  - `ingredients`: List of `Ingredient` objects
  - `time`: Time to cook minutes, integer
- Returns:
  - `200 OK` response when a new record was successfully created.
  - `400 Bad Request` response when provided fields are invalid.
  - `404 Not Found` response when an unknown recipe ID was provided.

Example response:
```json
{
    "success": true,
    "result": {
        "id": 1,
        "name": "Pizza",
        "procedure": "Est qui alias molestias facilis et et eum. Ducimus est corrupti et qui. Et quidem nostrum qui ipsum perspiciatis et enim. Odio impedit et unde voluptatem.",
        "time": 30,
        "ingredients": []
    }
}
```

### `DELETE /recipes/<recipe_id>`

- Deletes a recipe.
- Required headers:
  - `Authorization` header with bearer token that has `delete:recipes` permission.
- Request path argument: `recipe_id`
- Returns:
  - `200 OK` response when a new record was successfully created.
  - `404 Not Found` response when an unknown recipe ID was provided.

Example response:
```json
{
    "success": true,
    "recipe_id": 1
}
```

### `GET /ingredients`

- Returns the list of ingredients.
- Required headers:
  - `Authorization` header with bearer token that has `read:recipes` permission.
- Request arguments: None
- Returns:
  - `200 OK` response, body with a `result` key, value being the list of ingredients.

Example response:
```json
{
  "result": [
    {
        "id": 1,
        "recipe_id": 1,
        "name": "Flour",
        "optional": false,
        "measurement": 250,
        "measurement_unit": "grams"
    }
  ]
}
```

### `GET /ingredients/<item_id>`

- Returns a single ingredient.
- Required headers:
  - `Authorization` header with bearer token that has `read:recipes` permission.
- Request path arguments: `item_id`
- Returns:
  - `200 OK` response, body with a `result` key, value being the ingredient object.
  - `404 Not Found` response when an unknown ingredient ID was provided.

Example response:
```json
{
    "result": {
        "id": 1,
        "recipe_id": 1,
        "name": "Flour",
        "optional": false,
        "measurement": 250,
        "measurement_unit": "grams"
    }
}
```

### `POST /ingredients`

- Adds a new ingredient.
- Required headers:
  - `Authorization` header with bearer token that has `create:recipes` permission.
- Request body:
  - `recipe_id`: Related recipe ID
  - `name`: Ingredient name
  - `optional`: Whether the ingredient is optional, boolean
  - `measurement`: Measurement value, integer
  - `measurement_unit`: Measurement unit name
- Returns:
  - `200 OK` response when a new record was successfully created.
    `400 Bad Request` response when provided fields were invalid.

Example response:
```json
{
    "success": true,
    "result": {
        "id": 1,
        "ingredients": [],
        "name": "Pizza",
        "procedure": "Est qui alias molestias facilis et et eum. Ducimus est corrupti et qui. Et quidem nostrum qui ipsum perspiciatis et enim. Odio impedit et unde voluptatem.",
        "time": 30
    }
}
```

### `PATCH /ingredients/<item_id>`

- Updates an ingredient.
- Required headers:
  - `Authorization` header with bearer token that has `update:recipes` permission.
- Request body (can be a subset of):
  - `recipe_id`: Related recipe ID
  - `name`: Ingredient name
  - `optional`: Whether the ingredient is optional, boolean
  - `measurement`: Measurement value, integer
  - `measurement_unit`: Measurement unit name
- Returns:
  - `200 OK` response when the record was successfully updated.
  - `400 Bad Request` response when provided fields were invalid.
  - `404 Not Found` response when an unknown ingredient ID was provided.

Example response:
```json
{
    "success": true,
    "result": {
        "id": 1,
        "recipe_id": 1,
        "name": "Flour",
        "optional": false,
        "measurement": 250,
        "measurement_unit": "grams"
    }
}
```

### `DELETE /ingredients/<item_id>`

- Deletes an ingredient.
- Required headers:
  - `Authorization` header with bearer token that has `delete:recipes` permission.
- Request path arguments: `item_id`
- Returns:
  - `200 OK` response when a new record was successfully created.
  - `404 Not Found` response when an unknown recipe ID was provided.

Example response:
```json
{
    "success": true,
    "ingredient_id": 1
}
```

## Authentication and Permissions

Authentication is handled via [Auth0](https://auth0.com).

All except one endpoints require authentication, and proper permission. The root is a public endpoint left there for debugging.

Caveat: Currently the app does not offer a frontend with a login flow. For testing purposes, the access tokens are generated from two Machine-to-Machine apps' authentication using `client_credentials` grant type. The two apps are assigned permissions and act as users with ReadOnly and Admin roles.

API endpoints use these permissions:

* 'create:recipe' (can add recipes and ingredients)
* 'read:recipe' (can read recipes and ingredients)
* 'update:recipe' (can update recipes and ingredients)
* 'delete:recipe' (can delete recipes and ingredients)

### How to renew access tokens used in tests

Replace `client_id` and `client_secret` values.

```
curl --request POST \
  --url https://recipehub.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"your_client_id","client_secret":"your_client_secret","audience":"recipehub-api","grant_type":"client_credentials"}' | jq .access_token
```

For reference, see the Test tab of your Auth0 API.