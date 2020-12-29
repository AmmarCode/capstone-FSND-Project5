# Coffee Shop API

## Full Stack Nano - IAM Final Project
This is a Coffee Shop API, Hosted live on heroku: https://capstone-coffee.herokuapp.com/
1) Allows the shop barista to see the available drinks and desserts.
2) Allows the shop managers to perform CRUD actions for Drinks and Desserts.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is recommend to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `starter` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.
- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `starter` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Roles
### Roles and Users created and configured using Auth0
#### Manager 
* Have permission for GET - POST - PACTH - DELETE endpoints.

#### Barista
* Have permission for GET endpoints only.


## API
### Drinks
#### GET/drinks
```
{
    "drinks": [
        {
            "id": 1,
            "title": "Espresso"
        },
        {
            "id": 2,
            "title": "Cappuccino"
        }
    ],
    "success": true
}
```

#### POST/drinks
```
{
    "drinks": [
        {
            "id": 3,
            "title": "Water"
        }
    ],
    "success": true
}
```

#### PATCH/drinks/3
```
{
    "drinks": [
        {
            "id": 3,
            "title": "Updated Water"
        }
    ],
    "success": true
}
```

#### DELETE/drinks/3
```
{
    "delete": "3",
    "success": true
}
```

###Desserts
#### GET/desserts
```
{
    "drinks": [
        {
            "id": 1,
            "title": "Chocolate Brownie"
        },
        {
            "id": 2,
            "title": "Cinnamon Roll"
        }
    ],
    "success": true
}
```

#### POST/desserts
```
{
    "drinks": [
        {
            "id": 3,
            "title": "Chocolate Cookie"
        }
    ],
    "success": true
}
```

#### PATCH/desserts/3
```
{
    "drinks": [
        {
            "id": 3,
            "title": "Updated Cookie"
        }
    ],
    "success": true
}
```

#### DELETE/desserts/3
```
{
    "delete": "3",
    "success": true
}
```
