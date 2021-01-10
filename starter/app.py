import json
import os
from functools import wraps
from os import environ as env

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import (Flask, abort, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from six.moves.urllib.parse import urlencode
from werkzeug.exceptions import HTTPException

import constants
from auth import (AuthError, get_token_auth_header, requires_auth,
                  verify_decode_jwt)
from models import Dessert, Drink, setup_db

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = constants.SECRET_KEY
    CORS(app)
    setup_db(app)

    @app.errorhandler(Exception)
    def handle_auth_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (
            ex.code if isinstance(ex, HTTPException) else 500)
        return response

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    def requires_auth0(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if constants.PROFILE_KEY not in session:
                return redirect('/login')
            return f(*args, **kwargs)

        return decorated

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        token = auth0.authorize_access_token()
        session['token'] = token['access_token']
        print(session['token'])

        resp = auth0.get('userinfo')
        userinfo = resp.json()

        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/dashboard')

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

    @app.route('/logout')
    def logout():
        session.clear()
        params = {'returnTo': url_for(
            'home', _external=True), 'client_id': AUTH0_CLIENT_ID}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    @app.route('/dashboard')
    @requires_auth0
    def dashboard():
        return render_template('dashboard.html',
                               userinfo=session[constants.PROFILE_KEY],
                               userinfo_pretty=json.dumps(session[constants.
                               JWT_PAYLOAD], indent=4), token=session['token'])

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

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port=env.get('PORT', 3000), debug=True)
