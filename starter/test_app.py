import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Dessert, Drink, setup_db


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
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

        self.manager_token = {"Authorization": "bearer {}".format("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNTV3cyRHVPdFFyMlA2SE9aM1Y2biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWoudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmY2Q2ZGI1MDVhZWIzMDA3NWQ3M2ExOSIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTYwODgzNDM5NiwiZXhwIjoxNjA4OTIwNzk2LCJhenAiOiJ6d0w5WXhaSWM1VDNseFVScHNOODF6aUhnT1hsMlYyRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRlc3NlcnRzIiwiZGVsZXRlOmRyaW5rcyIsImdldDpkZXNzZXJ0cyIsImdldDpkcmlua3MiLCJwYXRjaDpkZXNzZXJ0cyIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZGVzc2VydHMiLCJwb3N0OmRyaW5rcyJdfQ.T0xufg1zAhgnPgknpoIc9ml146sC3S67CTDcgDejW2uYJo5HvngYK1_uSAv1ioZtNnfTskS6IakGQ6DNqY86-E5m_pAjfBmleVUmkl133tNQEoLI2nSPJcMe-K6n2sqwyruMiBsskhjlKuGWhcPkanV99jVAjyZEA9vhPLWH-1NR4uAbtxVW_P5FiUhAw_Re2gAlnbqUiFqTTf7uhBPeMT3LTWPxMgc55h66bZdy82UPNbEJmiUWQOiSWjWk9hL4ekIeX5fzS_HDJeiXEOc7sL2LoDn7eYbTT8vwSFNA26DS1rtTFD_d-6Empifobd5Dvu-S_rqyky3omFTMsq2xRQ")}

        self.barista_token = {"Authorization": "bearer {}".format("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNTV3cyRHVPdFFyMlA2SE9aM1Y2biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWoudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmY2Q2ZTA0OTE0OTE2MDA3ODBkMDkxOCIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTYwODc5Nzk2MSwiZXhwIjoxNjA4ODg0MzYxLCJhenAiOiJ6d0w5WXhaSWM1VDNseFVScHNOODF6aUhnT1hsMlYyRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRlc3NlcnRzIiwiZ2V0OmRyaW5rcyJdfQ.Tt6ixGfkFmZoa8v3_zzrUj6n11oBQeImSr0Q-AFoDZYM4dL2gX69xFo8_OMpLlxhYZlF_LW8pAMuF_V81zcgUGXHfRRs1RopvaryLfMe6lyb9J9HHGW3beAqAPHwcqEkPs-71afLFDpYs9GafdqjWhy5TKX0h_Hcz46Gq-G-d7cfqyK9P6g__wUsVilL9VQ5GVz2opluynY1F-Clasc4URMOHO0oavP0m-KsuhsMkseFes5k-89phESSX7Sd8UOZTdhbU59zMr-on6k5V9mKnO9Tj01oQ0kFnvFF55-qOuysWjwukp8YiLGeBbNV0ivmdWQ0Vnopohc6vChjJ_QWcw")}

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
        res = self.client().patch('/drinks/3', json=self.update_drink,
                                  headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_dessert(self):
        """Test update dessert"""
        res = self.client().patch('/desserts/3', json=self.update_dessert,
                                  headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_drink(self):
        """Test delete drink"""
        res = self.client().delete('/drinks/2', headers=self.manager_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_dessert(self):
        """Test delete dessert"""
        res = self.client().delete('/desserts/2', headers=self.manager_token)
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
