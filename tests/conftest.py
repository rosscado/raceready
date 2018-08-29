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
def resource_name():
	''' The name of the resource, e.g. 'events' in '/api/events/'
	Developers must override this abstract function in their own test module(s)
	to generate test fixtures for their resource type(s).
	'''
	raise NotImplementedError("Override resource_name function to return name of your resource collection, e.g. 'events'")
	return '{resources}'

@pytest.fixture
def resource_data():
	''' A dictionary of fields that can be used to instantiate a resource. The POST request payload.
	Developers must override this abstract function in their own test module(s)
	to generate test fixtures for their resource type(s).
	'''
	raise NotImplementedError("Override resource_data function to return a dict for your resource, e.g. {'title': 'foo bar'}")

@pytest.fixture
def required_fields():
	'''A list of the fieldnames required by the resource's data model
	Developers must override this abstract function in their own test module(s)
	to generate test fixtures for their resource type(s).'''
	raise NotImplementedError("Override required_fields function to return a list of required fields for your resource, e.g. ['title']")

@pytest.fixture
def resource_fixture(client, resource_name, resource_data):
	'''POST a resource for use in test cases and return its JSON object
	Assumes that the `test_post_{resource}` testcase passes
	'''
	post_rv = client.post('/api/{resource}/'.format(resource=resource_name), json=resource_data)
	resource_result = post_rv.get_json()
	yield resource_result

	client.delete('/api/{resource}/{id}'.format(resource=resource_name, id=resource_result['id']))
