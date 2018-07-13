import pytest

from hello import hello

@pytest.fixture
def client():
	hello.app.config['TESTING'] = True
	client = hello.app.test_client()

	yield client

def test_welcome(client):
	"""Test application root includes a generic greeting"""
	rv = client.get('/')
	assert b'Welcome' in rv.data

def test_get_visitors(client):
	"""Test visitors api"""
	rv = client.get('/api/visitors')
	json_resp = rv.get_json()
