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

@pytest.fixture
def resource_fixture(client):
	'''POST a resource for use in test cases and return its JSON object
	Assumes that the `test_post_{resource}` testcase passes
	Developers must override this abstract `resource_fixture` function in their
	own test module(s) to generate test fixtures for their resource type(s)
	This abstract method raises a NotImplementedError if called. Logic statements
	are included as override examples only.
	'''
	raise NotImplementedError("Override resource_fixture function in your test module to generate test fixtures for your resource type")
	resource_input = {}
	post_rv = client.post('/api/{resource}/', json=event_input)
	resource_result = post_rv.get_json()
	yield resource_result

	client.delete('/api/{resource}/{id}'.format(id=resource_result['id']))
