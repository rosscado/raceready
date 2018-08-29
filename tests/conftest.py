'''This module defines pytest fixtures available to all test files
Read more at https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
'''
import pytest
from context import app # check sys.path if this fails

@pytest.fixture
def client():
	'''A werkzeug.test.Client exposed by the Flask app for making HTTP requests
	to the application's REST API endpoints'''
	app.app.config['TESTING'] = True
	app.app.config['DATABASE'] = 'unittests'
	client = app.app.test_client()

	yield client
