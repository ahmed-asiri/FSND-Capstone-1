# RecipeHub

API for managing your recipes.

Heroku deployment: <insert URL here>

## Getting Started

Install dependencies

```
pip install -r requirements.txt
```

Start the app locally:

```
source setup.sh
flask run --reload
```

## Testing

```
pytest test_app.py
```

## Endpoints

Documentation of endpoints.

## Authentication and Permissions

Authentication is handled via Auth0.

API endpoints use these permissions:

* 'create:recipe' (can add recipes - also ingredients - items are read only*)
* 'read:recipe' (can read recipes, ingredients, and items)
* 'update:recipe' (can update recipes and ingredients)
* 'delete:recipe' (can delete recipes and ingredients)

(* Items are handled by fixtures, and are read-only. There's no related actions for them.)
