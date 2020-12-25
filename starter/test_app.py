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

        self.manager_token = {"Authorization": "bearer {}".format("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNTV3cyRHVPdFFyMlA2SE9aM1Y2biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWoudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmY2Q2ZGI1MDVhZWIzMDA3NWQ3M2ExOSIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTYwODkxOTAzOSwiZXhwIjoxNjA5MDA1NDM5LCJhenAiOiJ6d0w5WXhaSWM1VDNseFVScHNOODF6aUhnT1hsMlYyRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRlc3NlcnRzIiwiZGVsZXRlOmRyaW5rcyIsImdldDpkZXNzZXJ0cyIsImdldDpkcmlua3MiLCJwYXRjaDpkZXNzZXJ0cyIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZGVzc2VydHMiLCJwb3N0OmRyaW5rcyJdfQ.sGG9waNTCtR3pxxNCl6yiraPklHJWvdQUD7Q8SN9KU0CaUNr_HYskvb17OD8dnW-MNJMqMp849aRfFNgVwZNxkJiLmkfZ7xz4erXeOiDR7K9O_EvcAd0yx-TiFLKAcqjdFalyypu4yKC4O6FhMAIfUlrofbXiUGAfiivCzTYOAo5kqTRKGwUAtH7JvfHGDKF8w6qxL75Lfat60Uoxo2JOJqu23Roi3-RUzjjKoGpka9cHjGU1n3XOQaoofuAIMVgHTi-dNjxyEUboPlFlD2jutZnWnaUoecqhVoj9EUimduQY9Yow_lJMtFxF4Xo0CU0J5ti4FBLAiIGvL6YGwxvAw")}

        self.barista_token = {"Authorization": "bearer {}".format("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNTV3cyRHVPdFFyMlA2SE9aM1Y2biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWoudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmY2Q2ZTA0OTE0OTE2MDA3ODBkMDkxOCIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTYwODkxOTM3NywiZXhwIjoxNjA5MDA1Nzc3LCJhenAiOiJ6d0w5WXhaSWM1VDNseFVScHNOODF6aUhnT1hsMlYyRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRlc3NlcnRzIiwiZ2V0OmRyaW5rcyJdfQ.dSnCMKz4AUHqJ6_Yw-T2wRVi_CZh0XZ33KsOMUf54ntX2kl61CGXOYBYamSG-bVLrgmNOFoAU1aNDDhcP3-7mrrSoSnLedQQBqVMa3HfsInfC7MHVBP6NhfGxXz3TzmH9q1w77olJxT7XuP30bM5cYyzttXQfUma2uNztKsGtTUsshs3VMEL5G--ddQ40Oz3QTC3dHTZ61AZ8BtsMZVi3PdCqCMUpHAtV3KY6JG3weokdEmpLwPS8OFWqRslJUI2A4rvwL6lLQq2ru0CTKDTrX9cGv_rXSBXoPZPEDwErEvEZFoNApKgYl5WY84YETFy73omuqLZAdVMAflrcUlX6g")}

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
