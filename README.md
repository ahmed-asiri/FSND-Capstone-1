# RecipeHub

API for managing your cooking recipes.

Live Heroku deployment: https://fsnd-recipehub.herokuapp.com/recipes

## Authentication when using live deployment

The Heroku deployment requires authentication to start using. There are two access levels: ReadOnly and Admin.

For testing the live deployment, a Postman collection with access tokens is provided for convenience. Please see the **Testing** section about automated testing.

<todo: add the Postman collection with access tokens>

For details on access permissions, please see the **Authentication and Permissions** section later in the document.

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

First, you need a Heroku account and install the heroku client. Please see [the official docs](https://devcenter.heroku.com/) on how to do these.

<todo: insert instructions on how to setup app anew>

## Testing

There is a `DISABLE_AUTH0` environment variable that's used in testing.
The main reasons to disable authentication are to avoid spamming Auth0 with our test requests, and keep the main functionality tests shorter.

The app functionality tests are in `test_app.py`. This test module uses `DISABLE_AUTH0=1` setting.

```
pytest test_app.py
```

The access control tests make requests to Auth0, and should be run every so often. This test module unsets `DISABLE_AUTH0` variable.

```
pytest test_rbac.py
```

## Endpoints

Documentation of endpoints.

<todo: insert endpoints documentation>

## Authentication and Permissions

Authentication is handled via Auth0.

All except one endpoints require authentication, and proper permission. The root is a public endpoint left there for debugging.

Caveat: Currently the app does not offer a frontend with a login flow. For testing purposes, the access tokens are generated from two Machine-to-Machine apps' authentication using `client_credentials` grant type. The two apps are assigned permissions and act as users with ReadOnly and Admin roles.

API endpoints use these permissions:

* 'create:recipe' (can add recipes and ingredients)
* 'read:recipe' (can read recipes and ingredients)
* 'update:recipe' (can update recipes and ingredients)
* 'delete:recipe' (can delete recipes and ingredients)
