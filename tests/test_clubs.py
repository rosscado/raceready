import pytest
from resource import ResourceTestCase
from context import app # check sys.path if this fails

arbitrary_title='Unit test club' # default club fixture title
arbitrary_url='http://www.clontarfcc.com/' # default club fixture url

@pytest.fixture
def client():
	app.app.config['TESTING'] = True
	app.app.config['DATABASE'] = 'unittests'
	client = app.app.test_client()

	yield client

# test fixture generator functions, called by test cases as needed
@pytest.fixture
def club_fixture(client):
	'''Create and return a club for use in test cases
	Assumes that the `test_post_clubs` testcase passes'''
	club = {'title': arbitrary_title, 'url': arbitrary_url}
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

class TestClubs(ResourceTestCase):
	ns = '/api/clubs/'

	def test_get_clubs_not_empty(self, client, club_fixture):
		"""Test GET /clubs API for clubs listing when clubs do exist"""
		self._test_get_resources_not_empty(client, club_fixture)

	def test_post_clubs(self, client):
		'''Test POST /clubs API for club creation'''
		club_fixture = {
			'title': arbitrary_title,
			'url': arbitrary_url
		}

		self._test_post_resource(client, club_fixture)

	def test_post_clubs_required_fields(self, client):
		'''Test POST /clubs API for club creation when missing required fields'''
		club_fixture = {'title': arbitrary_title}

		self._test_post_resource_required_fields(client, club_fixture)

	def test_get_club(self, client, club_fixture):
		"""Test GET /clubs/{id} API"""
		self._test_get_resource(client, club_fixture)

	def test_put_club(self, client, club_fixture):
		"""Test PUT /clubs/{id} API for club modification"""
		club_fixture['title'] = "{original} modified".format(original=club_fixture['title'])
		self._test_put_resource(client, club_fixture)

	def test_put_club_not_found(self, client):
		"""Test PUT /clubs/{id} API with a non-existent {id}"""
		no_such_club_fixture = {'title': 'foo bar'}
		self._test_put_resource_not_found(client, no_such_club_fixture)

	def test_put_club_required_fields(self, client, club_fixture):
		"""Test PUT /clubs/{id} API for club modification when required fields are missing"""
		club_fixture_min = {
			'title': club_fixture['title']
			}
		self._test_put_resource_required_fields(client, club_fixture['id'], club_fixture_min)

	def test_delete_club(self, client, club_fixture):
		"""Test DELETE /clubs/{id} API for club deletion"""
		self._test_delete_resource(client, club_fixture)
