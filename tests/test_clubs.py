import pytest
from resource import ResourceTestCase
from context import app # check sys.path if this fails

arbitrary_title='Unit test club' # default club fixture title
arbitrary_url='http://www.clontarfcc.com/' # default club fixture url

@pytest.fixture
def resource_name():
	return 'clubs'

@pytest.fixture
def resource_data():
	return {
		'title': arbitrary_title,
		'url': arbitrary_url
	}

@pytest.fixture
def required_fields():
	return ['title']

def _get_resource_fixture(client, id):
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
	ns = '/api/{resources}/'.format(resources=resource_name())
