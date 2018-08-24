import pytest

from context import app # check sys.path if this fails

non_existent_id='007404007' # does not match an resource, reliably gives a 404

@pytest.fixture
def client():
	app.app.config['TESTING'] = True
	app.app.config['DATABASE'] = 'test_events'
	client = app.app.test_client()

	yield client

# test fixture generator functions, called by test cases as needed
def _post_event_fixture(client, title):
	'''Create and return an event for use in test cases
	Assumes that the `test_post_events` testcase passes'''
	event = {'title': title}
	post_rv = client.post('/api/events/', json=event)
	return post_rv.get_json()

def _get_event_fixture(client, id):
	'''Return an event for use in test cases
	Assumes that the `test_get_event` testcase passes
	and that an event with {id} has already been created.
	Returns None (does not raise an error) if event not found'''
	get_rv = client.get('/api/events/{id}'.format(id=id))
	if get_rv.status_code == 404:
		return None
	else:
		return get_rv.get_json()

# test assertion functions
def assert_list(obj):
	'''Return True iff obj is a list-like object'''
	assert 'index' in dir(obj) and 'append' in dir(obj)

# test case functions
def test_swagger(client):
	"""Test application root hosts swagger docs"""
	rv = client.get('/api/')
	assert b'swagger' in rv.data

def test_get_events(client):
	"""Test GET /events API for events listing"""
	rv = client.get('/api/events/')
	events_result = rv.get_json()
	assert events_result is not None
	assert_list(events_result)

def test_post_events(client):
	'''Test POST /events API for event creation'''
	event_fixture = {'title': 'The John Beggs'}

	rv = client.post('/api/events/', json=event_fixture)
	event_result = rv.get_json()
	assert event_result is not None
	assert event_result['title'] == event_fixture['title']
	assert 'id' in event_result

def test_get_event(client):
	"""Test GET /events/{id} API"""
	event_fixture = _post_event_fixture(client, 'GET Event Test')

	get_rv = client.get('/api/events/{id}'.format(id=event_fixture['id']))
	event_result = get_rv.get_json()
	assert event_result is not None
	assert 'id' in event_result and event_result['id'] == event_fixture['id']
	assert 'title' in event_result and event_result['title'] == event_fixture['title']

def test_get_event_not_found(client):
	"""Test GET /events/{id} API with a non-existent {id}"""
	get_rv = client.get('/api/events/{id}'.format(id=non_existent_id))
	assert get_rv.status_code == 404

def test_put_event(client):
	"""Test PUT /events/{id} API for event modification"""
	event_fixture = _post_event_fixture(client, 'PUT Event Test')
	event_fixture['title'] = "{original} modified".format(original=event_fixture['title'])

	put_rv = client.put('/api/events/{id}'.format(id=event_fixture['id']), json=event_fixture)
	assert put_rv.status_code == 204
	event_result = _get_event_fixture(client, event_fixture['id'])
	assert 'title' in event_result and event_result['title'] == event_fixture['title']

def test_put_event_not_found(client):
	"""Test PUT /events/{id} API with a non-existent {id}"""
	put_rv = client.put('/api/events/{id}'.format(id=non_existent_id), json={})
	assert put_rv.status_code == 404

def test_delete_event(client):
	"""Test DELETE /events/{id} API for event deletion"""
	event_fixture = _post_event_fixture(client, 'DELETE Event Test')

	delete_rv = client.delete('/api/events/{id}'.format(id=event_fixture['id']))
	assert delete_rv.status_code == 204
	event_result = _get_event_fixture(client, event_fixture['id'])
	assert event_result is None

def test_delete_event_not_found(client):
	"""Test DELETE /events/{id} API with a non-existent {id}"""
	delete_rv = client.delete('/api/events/{id}'.format(id=non_existent_id))
	assert delete_rv.status_code == 404
