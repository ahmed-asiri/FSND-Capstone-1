import os
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from models import setup_db, Recipe, Ingredient


def create_app(test_config=None):

    app = Flask(__name__)

    if not test_config:
        database_path = os.environ['DATABASE_URL']
        setup_db(app, database_path)
    else:
        setup_db(app, test_config['DATABASE_URL'])

    CORS(app)

    @app.route('/', methods=['POST', 'GET'])
    def health():
        return jsonify("Healthy")

    @app.route('/recipes', methods=['GET'])
    def list_recipes():
        result = [r.format() for r in Recipe.query.all()]
        return jsonify({
            'result': result
        })

    @app.route('/recipes', methods=['POST'])
    def add_recipe():
        try:
            data = request.get_json()
            recipe = Recipe(**data)
            recipe.insert()
            return jsonify({
                'success': True,
                'result': recipe.format()
            })
        except TypeError:
            abort(400)

    @app.route('/recipes/<int:recipe_id>', methods=['GET'])
    def get_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            abort(404)
        return jsonify({
            "result": recipe.format()
        })
    
    @app.route('/recipes/<int:recipe_id>', methods=['PATCH'])
    def update_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            abort(404)
        
        data = request.get_json()
        fields = ['name', 'procedure', 'time']
        has_valid_fields = any([field in data for field in fields])
        if not has_valid_fields:
            abort(400)
        
        for field in fields:
            if field in data:
                setattr(recipe, field, data[field])
        
        recipe.update()
        return jsonify({
            "success": True,
            "result": recipe.format()
        })

    @app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
    def delete_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            abort(404)
        
        recipe.delete()
        return jsonify({
            'success': True,
            'recipe_id': recipe_id
        })

    @app.route('/ingredients', methods=['GET'])
    def list_ingredients():
        result = [i.format() for i in Ingredient.query.all()]
        return jsonify({
            'result': result
        })

    
    @app.route('/ingredients', methods=['POST'])
    def create_ingredient():
        try:
            data = request.get_json()
            ingredient = Ingredient(**data)
            ingredient.insert()
            return jsonify({
                'success': True,
                'result': ingredient.format()
            })
        except TypeError:
            abort(400)
    
    @app.route('/ingredients/<int:item_id>', methods=['GET'])
    def get_ingredient(item_id):
        item = Ingredient.query.get(item_id)
        if not item:
            abort(404)
        return jsonify({
            "result": item.format()
        })
    
    @app.route('/ingredients/<int:item_id>', methods=['PATCH'])
    def update_ingredient(item_id):
        item = Ingredient.query.get(item_id)
        if not item:
            abort(404)
        
        data = request.get_json()
        fields = ['recipe_id', 'name', 'optional', 'measurement', 'measurement_unit']
        has_valid_fields = any([field in data for field in fields])
        if not has_valid_fields:
            abort(400)
        
        for field in fields:
            if field in data:
                setattr(item, field, data[field])
        
        item.update()
        return jsonify({
            "success": True,
            "result": item.format()
        })
    
    @app.route('/ingredients/<int:item_id>', methods=['DELETE'])
    def delete_ingredient(item_id):
        item = Ingredient.query.get(item_id)
        if not item:
            abort(404)
        
        item.delete()
        return jsonify({
            'success': True,
            'ingredient_id': item_id
        })

    # Error Handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        'message': 'Bad Request',
        'success': False
        }), 400


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        'message': 'Not Found',
        'success': False
        }), 404
  

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
        'message': 'Method Not Allowed',
        'success': False
        }), 405

  
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        'message': 'Unprocessable Entity',
        'success': False
        }), 422
    
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
        'message': 'Server Error',
        'success': False
        }), 500


    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
