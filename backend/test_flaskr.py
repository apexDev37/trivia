import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:postgres-admin@{}/{}'.format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # --- CATEGORIES

    def test_retrieve_all_categories_from_db(self):
        """
        Test that API method returns a response
        with all the categories in the database.
        """

        # Given
        endpoint = '/api/v1/categories'

        # When
        response = self.client().get(endpoint)
        data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertGreater(len(data['categories']), 0)

    # def test_404_when_no_categories_present_in_db(self):
    #     """
    #     Test that API endpoint returns a 404 error
    #     response when no categories are present in the database.
    #     """

    #     # Given
    #     endpoint = '/api/v1/categories'

    #     # When
    #     response = self.client().get(endpoint)
    #     data = json.loads(response.data)

    #     # Then
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertNotIn(data['categories'], data)
    #     self.assertGreater(data['message'], 'requested resource not found')

    def test_405_when_request_method_is_not_GET_on_categories_endpoint(self):
        """
        Test that API method returns a 405 error
        response when GET is not the request method on
        the API endpoint: '/api/v1/categories'.
        """

        # Given
        endpoint = '/api/v1/categories'

        # When
        response = self.client().post(endpoint)    
        data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertNotIn('categories', data, 'categories key should not be in data')
        self.assertEqual(data['message'], 'method not allowed')
    
    # --- QUESTIONS

    def test_200_when_retrieving_paginated_questions(self):
        """
        Test that API method returns a success
        response with all the questions in the db
        within valid pagination pages
        """

        # Given
        valid_page_number = 2
        endpoint = '/api/v1/questions?page={}'.format(valid_page_number)

        # When
        response = self.client().get(endpoint)
        data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertGreater(data['total_questions'], 0)

    
    def test_404_when_requesting_questions_beyond_valid_pagination_page(self):
        """
        Test that API method returns a 404 error
        response when questions beyond a valid
        pagination page are requested. 
        """

        # Given
        page_number = 570
        endpoint = '/api/v1/questions?page={}'.format(page_number)

        # When
        response = self.client().get(endpoint)
        data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'requested resource not found')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()