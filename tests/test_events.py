import pytest

from context import app # check sys.path if this fails

@pytest.fixture
def client():
	app.app.config['TESTING'] = True
	client = app.app.test_client()

	yield client

def test_swagger(client):
	"""Test application root hosts swagger docs"""
	rv = client.get('/api/')
	assert b'swagger' in rv.data

def test_get_events(client):
	"""Test events collection api"""
	rv = client.get('/api/events/')
	json_resp = rv.get_json()
	assert json_resp is not None
