import pytest

from context import app # check sys.path if this fails

@pytest.fixture
def client():
	app.app.config['TESTING'] = True
	app.app.config['DATABASE'] = 'test_events'
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
	assert verify_list(json_resp)

def test_post_events(client):
	'''Test event creation api'''
	event = {'title': 'The John Beggs'}

	rv = client.post('/api/events/', json=event)
	json_resp = rv.get_json()
	assert json_resp is not None
	assert json_resp['title'] == 'The John Beggs'

def verify_list(obj):
	'''Return True iff obj is a list-like object'''
	return 'index' in dir(obj) and 'append' in dir(obj)
