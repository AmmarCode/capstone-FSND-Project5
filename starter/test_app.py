import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Dessert, Drink, setup_db


database_path = os.environ['DATABASE_URL']

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        self.new_drink = {
            "title": "new drink"
        }

        self.update_drink = {
            "title": "updated drink"
        }

        self.new_dessert = {
            "title": "new dessert"
        }

        self.update_dessert = {
            "title": "updated dessert"
        }

        self.manager_token = {"Authorization": "bearer {}".format("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNTV3cyRHVPdFFyMlA2SE9aM1Y2biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWoudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmY2Q2ZGI1MDVhZWIzMDA3NWQ3M2ExOSIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTYwOTIxMTMzMywiZXhwIjoxNjA5Mjk3NzMzLCJhenAiOiJ6d0w5WXhaSWM1VDNseFVScHNOODF6aUhnT1hsMlYyRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRlc3NlcnRzIiwiZGVsZXRlOmRyaW5rcyIsImdldDpkZXNzZXJ0cyIsImdldDpkcmlua3MiLCJwYXRjaDpkZXNzZXJ0cyIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZGVzc2VydHMiLCJwb3N0OmRyaW5rcyJdfQ.BztvPK5_M99OpAtLhFDp99x_tfo2GDmIj5EceIKPaya-o_KZKlinbxbfgvBMMVhGNfSw9BZrycmWRnV8kU4A25N7zNFb9WYMXFL179SnECZSAGJF0HzYXebfU0z3zgr0uZRDQBwzWIhkjs5F9jNfQDuG0fbL5sUNbvlF-79O1fNTWhQTwVtF0iylJwvWrnBCSgT0Ymj4zf43SSeP3Sy27wisNeXZew2X4XpIOKkI--WpuZYNuNw5VhIH3OXtWMNjvuHZV9tJfKti_lh_dD8kzEEPVNlSg6vF4eIVesx31yCHv58Ahh9uoMlFGvj4espzDVL5FIVRhZY-ZlARmyJ4kA")}

        self.barista_token = {"Authorization": "bearer {}".format("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNTV3cyRHVPdFFyMlA2SE9aM1Y2biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWoudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmY2Q2ZTA0OTE0OTE2MDA3ODBkMDkxOCIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTYwOTIyMTcxOCwiZXhwIjoxNjA5MzA4MTE4LCJhenAiOiJ6d0w5WXhaSWM1VDNseFVScHNOODF6aUhnT1hsMlYyRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRlc3NlcnRzIiwiZ2V0OmRyaW5rcyJdfQ.UMz7KEdXnBFVbYvZpz0nPAIP-2fiLx1RFBmNNV882y5-RuJlz3tiiZVqfHIRalW7Rs9q-NFEmToOhCozujKtF_YXfPHSFfbvfB6raTF_JktBnQc7PQwDZm3cuiR-r7g2livQwu5M5f0i-rwNEOgRvXsApj7kElvizAJtTqThLv4J3s4rRysq6DlCxCNu1IRXKXIcP4JZzDV4ZR7CHpsLpTsD0s2gzQzRcx8P1tJ-uOqjy3nJXm-nIMDsFrmt4nXz2eGfmM5O9aLyfphOkpXJQcLnGOKrmZ_ZKMJmVJE3pc18udIx1NbVf1oPpZL7MI5mwjxPKis7TxpjZWjLA7MUMg")}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_post_new_drink(self):
        """Test post new drink"""
        res = self.client().post('/drinks', json=self.new_drink, headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_new_dessert(self):
        """Test post new dessert"""
        res = self.client().post('/desserts', json=self.new_dessert,
                                 headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_drinks_with_manager_token(self):
        """Test get drinks with manager token"""
        res = self.client().get('/drinks', headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_desserts_with_manager_token(self):
        """Test get desserts with manager token"""
        res = self.client().get('/desserts', headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_drinks_with_barista_token(self):
        """Test get drinks with barista token"""
        res = self.client().get('/drinks', headers=self.barista_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_desserts_with_barista_token(self):
        """Test get desserts with barista token"""
        res = self.client().get('/desserts', headers=self.barista_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_drink(self):
        """Test update drink"""
        res = self.client().patch('/drinks/5', json=self.update_drink,
                                  headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_dessert(self):
        """Test update dessert"""
        res = self.client().patch('/desserts/5', json=self.update_dessert,
                                  headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_drink(self):
        """Test delete drink"""
        res = self.client().delete('/drinks/4', headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_dessert(self):
        """Test delete dessert"""
        res = self.client().delete('/desserts/4', headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_401_get_drinks(self):
        """Test 401 get drinks"""
        res = self.client().get('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_401_get_desserts(self):
        """Test 401 get desserts"""
        res = self.client().get('/desserts')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_401_post_drink(self):
        """Test 401 post drink"""
        res = self.client().post('/drinks', json=self.new_drink)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_401_post_dessert(self):
        """Test 401 post dessert"""
        res = self.client().post('/desserts', json=self.new_dessert)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_401_update_drink(self):
        """Test 401 update drink"""
        res = self.client().patch('/drinks/1', json=self.update_drink)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_401_update_dessert(self):
        """Test 401 update dessert"""
        res = self.client().patch('/desserts/1', json=self.update_dessert)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_401_delete_drink(self):
        """Test 401 delete drink"""
        res = self.client().delete('/drinks/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_401_delete_dessert(self):
        """Test 401 delete dessert"""
        res = self.client().delete('/desserts/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_404_update_drink(self):
        """Test 404 update drink"""
        res = self.client().patch('/drinks/500', json=self.update_drink,
                                  headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_update_dessert(self):
        """Test 404 update dessert"""
        res = self.client().patch('/desserts/500', json=self.update_dessert,
                                  headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_delete_drink(self):
        """Test 404 delete drink"""
        res = self.client().delete('/drinks/500', headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_delete_desserts(self):
        """Test 404 delete dessert"""
        res = self.client().delete('/desserts/500', headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    unittest.main()
