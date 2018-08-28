import pytest

from context import app # check sys.path if this fails

non_existent_id='007404007' # does not match an resource, reliably gives a 404

@pytest.fixture
def client():
	app.app.config['TESTING'] = True
	app.app.config['DATABASE'] = 'unittests'
	client = app.app.test_client()

	yield client

# test fixture generator functions, called by test cases as needed
def _post_club_fixture(client, title, url=None):
	'''Create and return a club for use in test cases
	Assumes that the `test_post_clubs` testcase passes'''
	club = {'title': title}
	if url:
		club['url'] = url
	post_rv = client.post('/api/clubs/', json=club)
	return post_rv.get_json()

def _get_club_fixture(client, id):
	'''Return a club for use in test cases
	Assumes that the `test_get_club` testcase passes
	and that a club with {id} has already been created.
	Returns None (does not raise an error) if club not found'''
	get_rv = client.get('/api/clubs/{id}'.format(id=id))
	if get_rv.status_code == 404:
		return None
	else:
		return get_rv.get_json()

# test assertion functions
def assert_list(obj):
	'''Return True iff obj is a list-like object'''
	assert 'index' in dir(obj) and 'append' in dir(obj)

def test_get_clubs(client):
	"""Test GET /clubs API for clubs listing"""
	get_rv = client.get('/api/clubs/')
	assert get_rv.status_code == 200
	clubs_result = get_rv.get_json()
	assert clubs_result is not None
	assert_list(clubs_result)

def test_get_clubs_not_empty(client):
	"""Test GET /clubs API for clubs listing when clubs do exist"""
	club_fixture = _post_club_fixture(client, 'GET Clubs Test')

	get_rv = client.get('/api/clubs/')
	clubs_result = get_rv.get_json()
	assert clubs_result # assert that list is not None or empty

def test_post_clubs(client):
	'''Test POST /clubs API for club creation'''
	club_fixture = {
		'title': 'Clontarf Cycling Club',
		'url': 'http://www.clontarfcc.com'
	}

	post_rv = client.post('/api/clubs/', json=club_fixture)
	assert post_rv.status_code == 201
	club_result = post_rv.get_json()
	assert club_result is not None
	assert club_result['title'] == club_fixture['title']
	assert club_result['url'] == club_fixture['url']

def test_post_clubs_required_fields(client):
	'''Test POST /clubs API for club creation when missing required fields'''
	club_fixture = {} # missing required title field

	post_rv = client.post('/api/clubs/', json=club_fixture)
	assert post_rv.status_code == 400

	club_fixture['title'] = 'Title required field'
	post_rv = client.post('/api/clubs/', json=club_fixture)
	assert post_rv.status_code == 201

def test_get_club(client):
	"""Test GET /clubs/{id} API"""
	club_fixture = _post_club_fixture(client, 'GET Club Test')

	get_rv = client.get('/api/clubs/{id}'.format(id=club_fixture['id']))
	assert get_rv.status_code == 200
	club_result = get_rv.get_json()
	assert club_result is not None
	assert 'id' in club_result and club_result['id'] == club_fixture['id']
	assert 'title' in club_result and club_result['title'] == club_fixture['title']

def test_get_club_not_found(client):
	"""Test GET /clubs/{id} API with a non-existent {id}"""
	get_rv = client.get('/api/clubs/{id}'.format(id=non_existent_id))
	assert get_rv.status_code == 404

def test_put_club(client):
	"""Test PUT /clubs/{id} API for club modification"""
	club_fixture = _post_club_fixture(client, 'PUT club Test')
	club_fixture['title'] = "{original} modified".format(original=club_fixture['title'])

	put_rv = client.put('/api/clubs/{id}'.format(id=club_fixture['id']), json=club_fixture)
	assert put_rv.status_code == 204
	club_result = _get_club_fixture(client, club_fixture['id'])
	assert 'title' in club_result and club_result['title'] == club_fixture['title']

def test_put_club_not_found(client):
	"""Test PUT /clubs/{id} API with a non-existent {id}"""
	no_such_club_fixture = {'title': 'foo bar'}
	put_rv = client.put('/api/clubs/{id}'.format(id=non_existent_id), json=no_such_club_fixture)
	assert put_rv.status_code == 404

def test_put_club_required_fields(client):
	"""Test PUT /clubs/{id} API for club modification when required fields are missing"""
	club_fixture = _post_club_fixture(client, 'PUT club Test Required')

	del club_fixture['title']
	put_rv = client.put('/api/clubs/{id}'.format(id=club_fixture['id']), json=club_fixture)
	assert put_rv.status_code == 400

	club_fixture['title'] = 'Title restored'
	put_rv = client.put('/api/clubs/{id}'.format(id=club_fixture['id']), json=club_fixture)
	assert put_rv.status_code == 204

def test_delete_club(client):
	"""Test DELETE /clubs/{id} API for club deletion"""
	club_fixture = _post_club_fixture(client, 'DELETE club Test')

	delete_rv = client.delete('/api/clubs/{id}'.format(id=club_fixture['id']))
	assert delete_rv.status_code == 204
	club_result = _get_club_fixture(client, club_fixture['id'])
	assert club_result is None

def test_delete_club_not_found(client):
	"""Test DELETE /clubs/{id} API with a non-existent {id}"""
	delete_rv = client.delete('/api/clubs/{id}'.format(id=non_existent_id))
	assert delete_rv.status_code == 404
