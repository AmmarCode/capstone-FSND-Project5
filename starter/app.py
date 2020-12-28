import json
import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from auth import AuthError, requires_auth
from models import Dessert, Drink, setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    return app

app = create_app()


@app.route('/')
def index():
    return "Welcome to the Coffee Shop API"
@app.route('/drinks')
@requires_auth('get:drinks')
def view_drinks(jwt):
    try:
        drinks = Drink.query.all()
        if drinks is None:
            abort(404)
    except Exception as e:
        print(e)
    return jsonify({
        'success': True,
        'drinks': [drink.format() for drink in drinks]
    })
@app.route('/desserts')
@requires_auth('get:desserts')
def view_dessert(jwt):
    try:
        desserts = Dessert.query.all()
        if desserts is None:
            abort(404)
    except Exception as e:
        print(e)
    return jsonify({
        'success': True,
        'desserts': [dessert.format() for dessert in desserts]
    })
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = request.get_json()
    if body is None:
        abort(400)
    drink_title = body.get('title')
    drink = Drink(title=drink_title)
    drink.insert()
    return jsonify({
        'success': True,
        'drinks': [drink.format()]
    })
@app.route('/desserts', methods=['POST'])
@requires_auth('post:desserts')
def create_dessert(jwt):
    body = request.get_json()
    if body is None:
        abort(400)
    dessert_title = body.get('title')
    dessert = Dessert(title=dessert_title)
    dessert.insert()
    return jsonify({
        'success': True,
        'desserts': [dessert.format()]
    })
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    drink = Drink.query.get(id)
    if drink:
        try:
            body = request.get_json()
            new_title = body.get('title')
            if new_title:
                drink.title = new_title
            drink.update()
            return jsonify({
                'success': True,
                'drinks': [drink.format()]
            })
        except Exception as e:
            print(e)
            abort(422)
    else:
        abort(404)
@app.route('/desserts/<id>', methods=['PATCH'])
@requires_auth('patch:desserts')
def update_dessert(jwt, id):
    dessert = Dessert.query.get(id)
    if dessert:
        try:
            body = request.get_json()
            new_title = body.get('title')
            if new_title:
                dessert.title = new_title
            dessert.update()
            return jsonify({
                'success': True,
                'desserts': [dessert.format()]
            })
        except Exception as e:
            print(e)
            abort(422)
    else:
        abort(404)
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    drink = Drink.query.get(id)
    if drink:
        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)
    else:
        abort(404)
@app.route('/desserts/<id>', methods=['DELETE'])
@requires_auth('delete:desserts')
def delete_dessert(jwt, id):
    dessert = Dessert.query.get(id)
    if dessert:
        try:
            dessert.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)
    else:
        abort(404)
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404
@app.errorhandler(401)
def unauthorised(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorised"
    }), 401
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad_request"
    }), 400


if __name__ == "__main__":
    app.run(debug=True)